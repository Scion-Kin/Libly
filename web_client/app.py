#!/usr/bin/python3
''' This is the web server '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort,\
    session, request, redirect, url_for, make_response
from uuid import uuid4
import requests
import base64

app = Flask(__name__)

app.secret_key = 'hellolibly'

app.register_blueprint(client_view)

app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Use HttpOnly cookies


# Custom filter for Base64 encoding
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    ''' The home page route '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        keywords = request.form.get('keywords')

        headers = {"Content-Type": "application/json"}
        response = requests.post('https://usernet.tech/api/v1/search',
                                 headers=headers,
                                 json={"keywords": keywords})

        if response.status_code == 200:
            results = [i for i in response.json().values() if len(i) > 0]
            results = [item for sublist in results for item in sublist]

            authors = [item for item in results
                       if item["__class__"] == "Author"]

            books = [item for item in results
                     if item["__class__"] == "Book"]

            genres = [item for item in results
                      if item["__class__"] == "Genre"]

            users = [item for item in results
                     if item["__class__"] == "User"]

            if len(results) > 0:
                return render_template('search_results.html', found=True,
                                       authors=authors, books=books,
                                       genres=genres, users=users,
                                       keywords=keywords, uuid=uuid4(),
                                       pic=session["user_pic"])

            return render_template('search_results.html',
                                   authors=authors, books=books,
                                   genres=genres, users=users,
                                   keywords=keywords, uuid=uuid4(),
                                   found=False, pic=session["user_pic"])

    if session['user_type'] == 'librarian':
        return render_template('feed.html', admin=True,
                               pic=session["user_pic"], uuid=uuid4())

    else:
        if session["onboarded"] is False:
            return redirect(url_for('client_view.onboarding'))

        books = requests.get('https://usernet.tech/api/v1/hot/{}'
                             .format(session["user_id"])).json()

        if "error" not in books:
            return render_template('feed.html', admin=False, books=books[:5],
                                   uuid=uuid4(), pic=session["user_pic"],
                                   user_id=session["user_id"])

        return render_template('feed.html', uuid=uuid4(),
                               error="No books found in the database.",
                               pic=session["user_pic"])

    return render_template('index.html', uuid=uuid4())


@app.errorhandler(404)
def error_404(error):
    ''' Handles the 404 error '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    return make_response(render_template('errors.html', error="Not found",
                                         code=404, uuid=uuid4(),
                                         pic=session["user_pic"]), 404)


@app.errorhandler(500)
def error_500(error):
    ''' Handles the server error '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    return make_response(render_template('errors.html',
                                         error="Server error", code=500,
                                         uuid=uuid4(),
                                         pic=session["user_pic"]), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
