#!/usr/bin/python3
''' This is the view for email confirmation and account activation '''

from web_client.views import client_view
from flask import render_template
from uuid import uuid4
import requests

@client_view.route('/confirm/<string:user_id>', strict_slashes=False)
def confirmed_email(user_id):
    ''' activates the account of a user '''

    response = requests.get('https://usernet.tech/api/v1/users/confirm/{}'.format(user_id))
    if response.status_code == 404:
        return render_template('confirm_email.html', confirmed=False, title="Activation Failed")
    
    if response.status_code == 409:
        return render_template('confirm_email.html', confirmed=True, already=True,
                               title="Already activated!", uuid=uuid4())

    return render_template('confirm_email.html', confirmed=True, already=False,
                            title="Welcome", uuid=uuid4())
