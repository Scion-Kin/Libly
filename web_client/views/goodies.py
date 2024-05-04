#!/usr/bin/python3
''' This defines routes for some app goodies '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort, session, request, abort, redirect, url_for
from uuid import uuid4
import requests


@client_view.route('/hearted',  strict_slashes=False)
def hearted():
    ''' The favorites route '''

    if not session or session["logged"] == False:
        return redirect(url_for('home'))

    fav_authors = requests.get('http://localhost:5000/api/v1/{}/favs/authors'.format(session["user_id"]))
    if fav_authors.status_code == 200:
        fav_authors = fav_authors.json()
        all = []
        for i in fav_authors:
            author = requests.get('http://localhost:5000/api/v1/authors/{}'.format(i["author_id"])).json()
            all.append(author)
        fav_authors = all
    else:
        fav_authors = []

    fav_books = requests.get('http://localhost:5000/api/v1/{}/favs/books'.format(session["user_id"]))
    
    if fav_books.status_code == 200:
        fav_books = fav_books.json()
        all = []
        for i in fav_books:
            author = requests.get('http://localhost:5000/api/v1/books/{}'.format(i["book_id"])).json()
            all.append(author)
        fav_books = all
    else:
        fav_books = []

    fav_genres = requests.get('http://localhost:5000/api/v1/{}/favs/genres'.format(session["user_id"]))
    
    if fav_genres.status_code == 200:
        fav_genres = fav_genres.json()
        all = []
        for i in fav_genres:
            author = requests.get('http://localhost:5000/api/v1/genres/{}'.format(i["genre_id"])).json()
            all.append(author)
        fav_genres = all
    else:
        fav_genres = []

    return render_template('hearted.html', pic=session["user_pic"], fav_authors=fav_authors,
                           fav_books=fav_books, fav_genres=fav_genres)


@client_view.route('/hot', strict_slashes=False)
def hot():
    ''' The hot list route '''
