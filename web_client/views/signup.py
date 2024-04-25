#!/usr/bin/python3
''' The sign up route '''

from web_client.views import client_view
from flask import render_template, request, session, url_for, redirect
import requests


@client_view.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    ''' sign the user up '''

    if session and session['logged'] == True:
        return redirect(url_for('home'))

    if request.method == 'POST':

        headers = {"Content-Type": "application/json"}
        details = {
            "email": request.form.get('email'),
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "password": request.form.get('password')
        }
        response = requests.post('http://localhost:5000/api/v1/users', json=details, headers=headers)

        if response.status_code == 201:

            details = {
                "id": response.json()["id"],
                "first_name": response.json()["first_name"],
                "last_name": response.json()["last_name"],
                "email": response.json()["email"]
            }

            # send request to the node api to send the confirmation email
            response = requests.post('http://localhost:3000/signup', json=details, headers=headers)
            print(response.json())

            return redirect(url_for('client_view.login'))

        return render_template('signup.html', error=response.json()["error"])

    return render_template('signup.html')
