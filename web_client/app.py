#!/usr/bin/python3
''' This is the web server '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort, session, request, abort, redirect, url_for
from uuid import uuid4
import requests
import base64

app = Flask(__name__)

app.secret_key = 'hellolibly'

app.register_blueprint(client_view)

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # Set session lifetime to 30 days
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Use HttpOnly cookies


# Custom filter for Base64 encoding
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    ''' The home page route '''

    if session and session["logged"] == True:

        if request.method == 'POST':
            keywords = request.form.get('keywords')

            headers = {"Content-Type": "application/json"}
            response = requests.post('https://usernet.tech/api/v1/search', headers=headers, json={"keywords": keywords})

            if response.status_code == 200:
                results = [i for i in response.json().values() if len(i) > 0]
                results = [item for sublist in results for item in sublist]

                authors = [item for item in results if item["__class__"] == "Author"]
                books = [item for item in results if item["__class__"] == "Book"]
                genres = [item for item in results if item["__class__"] == "Genre"]
                users = [item for item in results if item["__class__"] == "User"]

                if len(results) > 0:
                    return render_template('search_results.html', authors=authors, books=books,
                                            genres=genres, users=users, keywords=keywords,
                                            found=True, pic=session["user_pic"])

                return render_template('search_results.html', authors=authors, books=books,
                                        genres=genres, users=users, keywords=keywords,
                                        found=False, pic=session["user_pic"])


        if session['user_type'] == 'librarian':
            return render_template('feed.html', admin=True, pic=session["user_pic"])

        else:
            books = requests.get('https://usernet.tech/api/v1/books').json()
            if "error" not in books:
                random = []

                count = 0
                for i in books:
                    if count == 2:
                        break
                    random.append(books[i]["data"])
                    count += 1

                return render_template('feed.html', admin=False, books=random, pic=session["user_pic"])
            return render_template('feed.html', error="No books found in the database.", pic=session["user_pic"])

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
