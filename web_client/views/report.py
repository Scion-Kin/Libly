#!/usr/bin/python3
''' The statistics page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for, request
import requests


@client_view.route('/statistics', methods=['GET', 'POST'], strict_slashes=False)
def get_statistics():
    ''' This queries the api for new database material '''
    if session and session['logged'] == True:

        if session["user_type"] != 'librarian':
            abort(404)

        if request.method == "POST":
            response = requests.get('https://usernet.tech/api/v1/report/{}'.
                                    format(request.form.get('days')))

            if response.status_code == 200:
                return render_template('stats.html', stats={
                                       "authors": response.json()["authors"],
                                       "books": response.json()["books"],
                                       "genres": response.json()["genres"],
                                       "reviews": response.json()["reviews"],
                                       "users": response.json()["users"]},
                                       pic=session["user_pic"], name=session["first_name"], days=request.form.get('days'))

            abort(500)

        return render_template('stats.html', pic=session["user_pic"], name=session["first_name"])

    return redirect(url_for('home'))


@client_view.route('/statistics/numbers', methods=['GET', 'POST'], strict_slashes=False)
def get_statistics_numbers():
    ''' The all authors page  '''
    if session and session['logged'] == True:

        if session["user_type"] != 'librarian':
            abort(404)

        if request.method == "POST":
            response = requests.get('https://usernet.tech/api/v1/report/{}'.
                                    format(request.form.get('days')))

            if response.status_code == 200:
                return render_template('stats.html', numbers={
                                       "authors": len(response.json()["authors"]),
                                       "books": len(response.json()["books"]),
                                       "genres": len(response.json()["genres"]),
                                       "reviews": len(response.json()["reviews"]),
                                       "users": len(response.json()["users"])},
                                       pic=session["user_pic"], name=session["first_name"], days=request.form.get('days'))

            abort(500)

        return render_template('stats.html', pic=session["user_pic"], name=session["first_name"])

    return redirect(url_for('home'))
