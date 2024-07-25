#!/usr/bin/python3
''' The login manager '''

from web_client.views import client_view
from flask import render_template, session, abort, \
    request, redirect, url_for, make_response
from uuid import uuid4
import requests


@client_view.route('/login', methods=['GET', 'POST'],
                   strict_slashes=False)
def login():
    ''' log the user in '''

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        response = requests.post('https://usernet.tech/api/v1/login',
                                 headers={'Content-Type': 'application/json'},
                                 json={"email": email, "password": password})

        if response.status_code != 200:
            return render_template('login.html',
                                   error=response.json()["error"],
                                   uuid=uuid4())

        else:
            user = response.json()["user"]
            session.permanent = True
            session["logged"] = True
            session["user_email"] = user["email"]
            session["user_id"] = user["id"]
            session["user_type"] = user["user_type"]
            session["onboarded"] = user["onboarded"]
            session["first_name"] = user["first_name"]
            session["middle_name"] = (user["middle_name"]
                                      if user["middle_name"] else ' ')
            session["last_name"] = user["last_name"]
            session["user_pic"] = user["pic"]

            # Create a response object with the redirection and set the cookie
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('user_id', user["id"], max_age=2592000)

            return resp

    return render_template("login.html", uuid=uuid4())


@client_view.route('/logout', methods=['GET'])
def clear_data():

    session.permanent = False
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('user_id')
    session.clear()
    return resp
