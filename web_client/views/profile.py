#!/usr/bin/python3
''' Defines a method for user profiles '''

from web_client.views import client_view
from flask import session, redirect, url_for, render_template, abort
from uuid import uuid4
import requests


@client_view.route('/profile/<string:user_id>', strict_slashes=False)
def profile(user_id):
    ''' Handels user profiling '''

    if not session or session["logged"] == False:
        return redirect(url_for('home'))

    user = requests.get('https://usernet.tech/api/v1/users/{}'.format(user_id))
    user = [user.json()[i] for i in user.json()][0]["data"] if user.status_code == 200 else abort(404)

    reviews = requests.get('https://usernet.tech/api/v1/users/{}/reviews'.format(user_id))
    reviews = reviews.json() if reviews.status_code == 200 else []

    fav_authors = requests.get('https://usernet.tech/api/v1/{}/favs/authors'.format(user_id))
    if fav_authors.status_code == 200:
        fav_authors = fav_authors.json()
        all = []
        for i in fav_authors:
            author = requests.get('https://usernet.tech/api/v1/authors/{}'.format(i["author_id"])).json()
            for j in author:
                all.append(author[j]["data"])

        fav_authors = all
    else:
        fav_authors = []

    fav_books = requests.get('https://usernet.tech/api/v1/{}/favs/books'.format(user_id))
    
    if fav_books.status_code == 200:
        fav_books = fav_books.json()
        all = []
        for i in fav_books:
            book = requests.get('https://usernet.tech/api/v1/books/{}'.format(i["book_id"])).json()
            for j in book:
                all.append(book[j]["data"])

        fav_books = all
    else:
        fav_books = []

    fav_genres = requests.get('https://usernet.tech/api/v1/{}/favs/genres'.format(user_id))
    
    if fav_genres.status_code == 200:
        fav_genres = fav_genres.json()
        all = []
        for i in fav_genres:
            genre = requests.get('https://usernet.tech/api/v1/genres/{}'.format(i["genre_id"])).json()
            for j in genre:
                all.append(genre[j]["data"])

        fav_genres = all
    else:
        fav_genres = []

    return render_template('profile.html', pic=session["user_pic"], authors=fav_authors,
                           books=fav_books, genres=fav_genres, reviews=reviews,
                           user=user, user_id=session["user_id"], uuid=uuid4())
