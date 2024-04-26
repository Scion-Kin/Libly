#!/usr/bin/python3
''' The user manager '''

from web_client.views import client_view
from flask import render_template, session, abort, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import os


@client_view.route('/settings', methods=['GET', 'POST'], strict_slashes=False)
def manage_user():
    ''' manage authors '''
    if session and session['logged'] == True:
        
        if request.method == 'POST':
            file = request.files['pic']
            headers = {"Content-Type": "application/json"}
            response = requests.post('http://localhost:5000/api/v1/users/{}'.format(request.form.get('id')),
                                     headers=headers, json={
                "first_name": request.form.get('first_name'), "middle_name": request.form.get('middle_name'),
                "last_name": request.form.get('last_name'), "pic": secure_filename(file.filename)
            })

            file.save(os.path.join('web_client/static/images', secure_filename(file.filename)))

            return redirect(url_for('client_view.manage_authors'))

        return render_template('settings.html', first_name=session["first_name"], last_name=session["last_name"],
                                email=session["user_email"], pic=session["user_pic"])
    return redirect(url_for('home'))

