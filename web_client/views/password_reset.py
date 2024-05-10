#!/usr/bin/python3
''' The password reset route '''

from web_client.views import client_view
from flask import render_template, request, session, url_for, redirect
from uuid import uuid4
import requests


@client_view.route('/reset', strict_slashes=False)
def request_reset():
    ''' user password reset '''

    return render_template('reset.html')
