#!/usr/bin/python3
''' This is the web server '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort, session, request
from itsdangerous import URLSafeSerializer
import requests


app = Flask(__name__)

app.secret_key = 'temporary_key'

s = URLSafeSerializer(app.secret_key)

app.register_blueprint(client_view)


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    ''' The home page route '''
    if request.method == 'POST':
        keywords = request.form.get('keywords')

        try:       
            headers = {"Content-Type": "application/json"}
            response = requests.post('http://0.0.0.0:5000/api/v1/search', headers=headers, json={"keywords": keywords})

            if response.status_code == 200:
                print('\n', response.json(), '\n')

                return render_template('search_results.html')

        except Exception:
            return render_template('search_results.html', error="Failed to reach server")

    if session and session['logged'] == True:
        return render_template('feed.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5050, debug=True)
