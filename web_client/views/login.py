#!/usr/bin/python3
''' The login manager '''

from web_client.views import client_view
from flask import render_template, session, abort, request, jsonify, redirect, url_for
from itsdangerous import URLSafeSerializer
from models import storage
from models.user import User


@client_view.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    ''' log the user in '''

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = [i for i in storage.all(User).values() if i.email == email]
        if len(user) < 1:
            return render_template('login.html', error='User not found')

        if password == user[0].password:
            session.permanent = True
            session["logged"] = True
            session["user_id"] = user[0].id
            session["user_type"] = user[0].user_type
            session["user_name"] = user[0].first_name + user[0].last_name

            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template("login.html")


@client_view.route('/logout', methods=['GET'])
def clear_data():

    session.permanent = False
    session.clear()
    return redirect(url_for('home'))
