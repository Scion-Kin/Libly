#!/usr/bin/python3
''' The author or genre page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for
from uuid import uuid4
import requests

from os import getenv
HOST = getenv('API_HOST')


@client_view.route('/author/<string:author_id>', strict_slashes=False)
def author(author_id):
    ''' The author page '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    response = requests.get('https://{}/api/v1/authors/{}'
                            .format(HOST, author_id))

    if response.status_code == 200:
        for i in response.json():
            book_list = response.json()[i]["book_list"]
            return render_template('author_genre.html',
                                   book_list=book_list,
                                   pic=session["user_pic"],
                                   uuid=uuid4(),
                                   data=response.json()[i]["data"],
                                   type="author")

        abort(404)


@client_view.route('/genre/<string:genre_id>', strict_slashes=False)
def genre(genre_id):
    ''' The genre page '''
    if not session and not session['logged']:

        return redirect(url_for('home'))

    response = requests.get('https://{}/api/v1/genres/{}'
                            .format(HOST, genre_id))

    if response.status_code == 200:

        for i in response.json():
            book_list = response.json()[i]["book_list"]
            return render_template('author_genre.html',
                                   book_list=book_list,
                                   pic=session["user_pic"],
                                   uuid=uuid4(),
                                   data=response.json()[i]["data"],
                                   type=genre)

    abort(404)
