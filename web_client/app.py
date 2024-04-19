#!/usr/bin/python3
''' This is the web server '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort, session, request, abort
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
                results = [i for i in response.json().values() if len(i) > 0]

                authors = results[0] if len(results) > 0 else []
                books = results[1] if len(results) > 1 else []
                genres = results[3] if len(results) > 3 else []
                users = results[2] if len(results) > 2 else []

                return render_template('search_results.html', authors=authors, books=books, genres=genres, users=users)

        except Exception:
            abort(500)

    if session and session['logged'] == True:
        return render_template('feed.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5050, debug=True)
