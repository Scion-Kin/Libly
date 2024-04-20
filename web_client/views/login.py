#!/usr/bin/python3
''' The log in route '''

from web_client.views import client_view
from flask import render_template, request, session, url_for, redirect
from models import storage
from models.user import User
from itsdangerous import URLSafeSerializer


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
            session["logged"] = True
            session["user_id"] = user[0].id
            session["user_type"] = user[0].user_type
            session["user_name"] = user[0].first_name + user[0].last_name

            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template("login.html")
