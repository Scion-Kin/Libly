#!/usr/bin/python3
''' This is the view for email confirmation and account activation '''

from web_client.views import client_view
from flask import render_template
from models import storage
from models.user import User
from uuid import uuid4

@client_view.route('/confirm/<string:user_id>', strict_slashes=False)
def confirmed_email(user_id):
    ''' activates the account of a user '''

    storage.reload()
    user = storage.get(User, user_id)
    if not user:
        return render_template('confirm_email.html', confirmed=False, title="Activation Failed")

    if user.confirmed is False:
        user.confirmed = True
        user.save()
        return render_template('confirm_email.html', confirmed=True, already=False,
                               title="Welcome!", uuid=uuid4())

    return render_template('confirm_email.html', confirmed=True, already=True,
                            title="Already Activated", uuid=uuid4())
