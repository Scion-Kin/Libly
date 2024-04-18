#!/usr/bin/python3
''' The log in route '''

from web_client.views import client_view
from flask import render_template, request, session, url_for, redirect


@client_view.route('/signup', strict_slashes=False)
def signup():
    ''' log the user in '''

    return render_template('signup.html')
