#!/usr/bin/python3
''' The user manager '''

from web_client.views import client_view
from flask import render_template, session, \
    request, redirect, url_for
from werkzeug.utils import secure_filename
from uuid import uuid4
import requests
import os

from os import getenv
HOST = getenv('API_HOST')


@client_view.route('/settings', methods=['GET', 'POST'],
                   strict_slashes=False)
def manage_user():
    ''' manage user '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        file = request.files['pic']

        details = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "password": request.form.get('old_password')
        }

        if file:
            details["pic"] = secure_filename(file.filename)

        if len(request.form.get('new_password')) > 0:
            details["new_password"] = request.form.get('new_password')

        headers = {"Content-Type": "application/json"}
        response = requests.put('https://{}/api/v1/users/{}'
                                .format(HOST, session['user_id']),
                                headers=headers, json=details)

        if response.status_code == 200:
            if file:
                if not os.path.exists('web_client/static/images/'):
                    os.makedirs('web_client/static/images/')
                    file.save(os.path.join('web_client/static/images/',
                              secure_filename(file.filename)))

            session['user_pic'] = secure_filename(file.filename) if file else session.get('user_pic')
            session['email'] = request.form.get('email', session.get('email'))
            session['first_name'] = request.form.get('first_name', session.get('first_name'))
            session['last_name'] = request.form.get('last_name', session.get('last_name'))
            session['middle_name'] = request.form.get('middle_name', session.get('middle_name', ' '))

            return redirect(url_for('home'))

        return render_template('settings.html',
                               first_name=session["first_name"],
                               last_name=session["last_name"], uuid=uuid4(),
                               error=response.json()["error"].capitalize(),
                               pic=session["user_pic"])

    return render_template('settings.html', first_name=session["first_name"],
                           uuid=uuid4(), last_name=session["last_name"],
                           pic=session["user_pic"])
