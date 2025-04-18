#!/usr/bin/python3
''' This is the view for email confirmation and account activation '''

from web_client.views import client_view
from flask import render_template
from uuid import uuid4
import requests

from os import getenv
HOST = getenv('API_HOST')

@client_view.route('/confirm/<string:user_id>', strict_slashes=False)
def confirmed_email(user_id):
    ''' activates the account of a user '''

    response = requests.get('https://{}/api/v1/users/confirm/{}'
                            .format(HOST, user_id))

    if response.status_code == 404:
        return render_template('confirm_email.html', confirmed=False,
                               title="Activation Failed")

    elif response.status_code == 409:
        return render_template('confirm_email.html', already=True,
                               title="Already activated!", uuid=uuid4())

    elif response.status_code != 200:
        return render_template('confirm_email.html', confirmed=False,
                               title="Activation Failed")

    return render_template('confirm_email.html', confirmed=True,
                           title="Welcome!", uuid=uuid4())
