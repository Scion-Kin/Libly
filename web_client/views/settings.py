#!/usr/bin/python3
''' The user manager '''

from web_client.views import client_view
from flask import render_template, session, abort, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import os


@client_view.route('/settings', methods=['GET', 'POST'], strict_slashes=False)
def manage_user():
    ''' manage user '''
    if session and session['logged'] == True:
        
        if request.method == 'POST':
            file = request.files['pic']
            if not file:
                return render_template('settings.html', error="No picture provided")

            details = {
                "email": request.form.get('email'),
                "first_name": request.form.get('first_name'), "middle_name": request.form.get('middle_name'),
                "last_name": request.form.get('last_name'), "pic": secure_filename(file.filename),
                "password": request.form.get('old_password'), "new_password": request.form.get('new_password')
            }

            for key, value in details.items():
                if key not in ["middle_name", "new_password"] and len(value) == 0:
                    return render_template('settings.html', first_name=session["first_name"], last_name=session["last_name"],
                                            error="Missing {}".format(value),
                                            pic=session["user_pic"])

            headers = {"Content-Type": "application/json"}
            response = requests.put('http://localhost:5000/api/v1/users/{}'.format(session['user_id']),
                                     headers=headers, json=details)

            if response.status_code == 200:
                file.save(os.path.join('web_client/static/images', secure_filename(file.filename)))

                return redirect(url_for('home'))

            return render_template('settings.html', first_name=session["first_name"], last_name=session["last_name"],
                                   error=response.json()["error"].capitalize(), pic=session["user_pic"])

        return render_template('settings.html', first_name=session["first_name"],
                               last_name=session["last_name"], pic=session["user_pic"])
    return redirect(url_for('home'))
