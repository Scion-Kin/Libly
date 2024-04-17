#!/usr/bin/python3
''' This is the web server '''

from flask import Flask, render_template
from models import storage
from models.user import User
import requests

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    ''' The home page route '''

    return render_template('index.html')


@app.route('/<string:user_id>/confirm', strict_slashes=False)
def confirm_email(user_id):
    ''' activates the account of a user '''

    req = requests.get('http://0.0.0.0:5000/api/v1/users/{}'.format(user_id))

    if req.status_code == 200:
        user = storage.get(User, user_id)
        if user.confirmed is False:
            user.confirmed = True
            user.save()

        return render_template('confirm_email.html', confirmed=True)

    return render_template('confirm_email.html', confirmed=False)


if __name__ == "__main__":
    app.run(port=5050, debug=True)
