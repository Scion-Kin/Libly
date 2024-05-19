#!/usr/bin/python3
''' Defines a route for book info '''

from web_client.views import client_view
from flask import render_template, session, request, redirect, url_for
from uuid import uuid4
import requests


@client_view.route('/about/book', methods=['GET', 'POST'],
                   strict_slashes=False)
def book_info():
    ''' The about book route '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if request.method == 'POST':

        response = requests.get('https://usernet.tech/api/v1/books/{}'
                                .format(request.form.get('id')))

        if response.status_code == 200:
            for i in response.json():

                reviews = requests.get('https://usernet.tech/api/v1/{}/reviews'
                                       .format(request.form.get('id')))

                if reviews.status_code == 200:
                    return render_template('info.html',
                                           info=response.json()[i]["data"],
                                           uuid=uuid4(),
                                           reviews=reviews.json(),
                                           pic=session["user_pic"])

                return render_template('info.html',
                                       info=response.json()[i]["data"],
                                       pic=session["user_pic"], uuid=uuid4())

    return render_template('info.html', pic=session["user_pic"], uuid=uuid4())
