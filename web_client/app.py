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

        print(keywords)

        try:       
            headers = {"Content-Type": "application/json"}
            response = requests.post('http://0.0.0.0:5000/api/v1/search', headers=headers, json={"keywords": keywords})

            if response.status_code == 200:
                results = [i for i in response.json().values() if len(i) > 0]
                results = [item for sublist in results for item in sublist]

                authors = [item for item in results if item["__class__"] == "Author"]
                books = [item for item in results if item["__class__"] == "Book"]
                genres = [item for item in results if item["__class__"] == "Genre"]
                users = [item for item in results if item["__class__"] == "User"]               

                if len(results) > 0:
                    return render_template('search_results.html', authors=authors, books=books, genres=genres, users=users, keywords=keywords, found=True)

                return render_template('search_results.html', authors=authors, books=books, genres=genres, users=users, keywords=keywords, found=False)

        except Exception:
            raise

    if session and session['logged'] == True:
        return render_template('feed.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5050, debug=True)
