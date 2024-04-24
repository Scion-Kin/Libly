#!/usr/bin/python3
''' The admin manager '''

from web_client.views import client_view
from flask import render_template, session, redirect, url_for
import requests
import os


@client_view.route('/read/<string:book_id', strict_slashes=False)
def read_book(book_id):
    ''' manage authors '''

    if session and session['user_type'] == 'king':

        data = requests.get(f'http://localhost:5000/api/v1/books/{book_id}')

        if data.status_code == 200:
            #for i in data.json():


            return render_template('read.html')

    return redirect(url_for('home'))
