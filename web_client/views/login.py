#!/usr/bin/python3
''' The login manager '''

from web_client.views import client_view
from flask import render_template, session, abort, request, jsonify, redirect, url_for, make_response
from itsdangerous import URLSafeSerializer
from models import storage
from models.user import User


@client_view.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    ''' log the user in '''

    storage.reload()

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = [i for i in storage.all(User).values() if i.email == email]
        if len(user) < 1:
            return render_template('login.html', error='User not found')

        if password == user[0].password:

            if user[0].confirmed == False:
                return render_template('login.html', error='You have not confirmed your email. Please check your email inbox and activate your account')

            session.permanent = True
            session["logged"] = True
            session["user_email"] = user[0].email
            session["user_id"] = user[0].id
            session["user_type"] = user[0].user_type
            session["first_name"] = user[0].first_name
            session["middle_name"] = user[0].middle_name if user[0].middle_name else ' '
            session["last_name"] = user[0].last_name
            session["user_pic"] = user[0].pic

            # Create a response object with the redirection and set the cookie
            resp = make_response(redirect('/'))
            resp.set_cookie('user_id', user[0].id, max_age=2592000)

            return resp
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template("login.html")


@client_view.route('/logout', methods=['GET'])
def clear_data():

    session.permanent = False
    session.clear()
    return redirect(url_for('home'))
