#!/usr/bin/python3
''' This defines routes for some app goodies '''

from web_client.views import client_view
from flask import render_template, session, redirect, url_for
from uuid import uuid4
import requests

from os import getenv
HOST = getenv('API_HOST')


@client_view.route('/hearted',  strict_slashes=False)
def hearted():
    ''' The favorites route '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    fav_authors = requests.get('https://{}/api/v1/{}/favs/authors'
                               .format(HOST, session["user_id"]))
    if fav_authors.status_code == 200:
        fav_authors = fav_authors.json()
        all = []
        for i in fav_authors:
            author = requests.get('https://{}/api/v1/authors/{}'
                                  .format(HOST, i["author_id"])).json()
            for j in author:
                all.append(author[j]["data"])

        fav_authors = all
    else:
        fav_authors = []

    fav_books = requests.get('https://{}/api/v1/{}/favs/books'
                             .format(HOST, session["user_id"]))

    if fav_books.status_code == 200:
        fav_books = fav_books.json()
        all = []
        for i in fav_books:
            book = requests.get('https://{}/api/v1/books/{}'
                                .format(HOST, i["book_id"])).json()
            for j in book:
                all.append(book[j]["data"])

        fav_books = all
    else:
        fav_books = []

    fav_genres = requests.get('https://{}/api/v1/{}/favs/genres'
                              .format(HOST, session["user_id"]))

    if fav_genres.status_code == 200:
        fav_genres = fav_genres.json()
        all = []
        for i in fav_genres:
            genre = requests.get('https://{}/api/v1/genres/{}'
                                 .format(HOST, i["genre_id"])).json()
            for j in genre:
                all.append(genre[j]["data"])

        fav_genres = all
    else:
        fav_genres = []

    return render_template('hearted.html',
                           pic=session["user_pic"], fav_authors=fav_authors,
                           fav_books=fav_books, fav_genres=fav_genres,
                           name=session["first_name"], uuid=uuid4())


@client_view.route('/hot', strict_slashes=False)
def hot():
    ''' The hot list route '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    hot = requests.get('https://{}/api/v1/hot/{}'
                       .format(HOST, session["user_id"]))

    return render_template('hot.html',
                           hot_books=hot.json(), name=session["first_name"],
                           pic=session["user_pic"], uuid=uuid4())
