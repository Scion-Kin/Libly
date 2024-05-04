#!/usr/bin/python3
''' The author or genre page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for
from uuid import uuid4
import requests


@client_view.route('/authors', strict_slashes=False)
def authors():
    ''' The all authors page  '''
    if session and session['logged'] == True:
        response = requests.get('https://usernet.tech/api/v1/authors/')

        if response.status_code == 200:
            data = [response.json()[i]["data"] for i in response.json()]
            return render_template('resource_list.html',
                                    all=data, uuid=uuid4(),
                                    type="Authors", pic=session["user_pic"]) 

        abort(500)

    return redirect(url_for('home'))

@client_view.route('/books', strict_slashes=False)
def books():
    ''' The author page  '''
    if session and session['logged'] == True:
        response = requests.get('https://usernet.tech/api/v1/books/')

        if response.status_code == 200:
            data = [response.json()[i]["data"] for i in response.json()]
            return render_template('resource_list.html',
                                       all=data, uuid=uuid4(),
                                       type="Books", pic=session["user_pic"]) 

        abort(500)

    return redirect(url_for('home'))

@client_view.route('/genres', strict_slashes=False)
def genres():
    ''' The author page  '''
    if session and session['logged'] == True:
        response = requests.get('https://usernet.tech/api/v1/genres/')

        if response.status_code == 200:
            data = [response.json()[i]["data"] for i in response.json()]
            return render_template('resource_list.html',
                                       all=data, uuid=uuid4(),
                                       type="Genres", pic=session["user_pic"]) 

        abort(500)

    return redirect(url_for('home'))
