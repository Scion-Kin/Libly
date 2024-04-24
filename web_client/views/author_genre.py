#!/usr/bin/python3
''' The author or genre page '''

from web_client.views import client_view
from flask import render_template, abort, session
import requests


@client_view.route('/author/<string:author_id>', strict_slashes=False)
def author(author_id):
    ''' The author page  '''
    if session and session['logged'] == True:
        response = requests.get(f'http://localhost:5000/api/v1/authors/{author_id}')

        if response.status_code == 200:
            for i in response.json():
                return render_template('author_genre.html',
                                       book_list=response.json()[i]["book_list"],
                                       data=response.json()[i]["data"], type="author") 

        abort(404)

    return redirect(url_for('home'))


@client_view.route('/genre/<string:genre_id>', strict_slashes=False)
def genre(genre_id):
    ''' The genre page '''
    if session and session['logged'] == True:
        response = requests.get(f'http://localhost:5000/api/v1/genres/{genre_id}')

        if response.status_code == 200:
            
            for i in response.json():
                return render_template('author_genre.html',
                                       book_list=response.json()[i]["book_list"],
                                       data=response.json()[i]["data"], type=genre) 

        abort(404)

    return redirect(url_for('home'))
