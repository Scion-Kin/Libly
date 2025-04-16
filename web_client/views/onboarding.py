#!/usr/bin/python3
''' Defines a route for user onboarding '''

from web_client.views import client_view
from flask import render_template, session, request, \
    redirect, url_for
from uuid import uuid4
import requests

from os import getenv
HOST = getenv('API_HOST')

@client_view.route('/onboarding', methods=['GET', 'POST'],
                   strict_slashes=False)
def onboarding():
    ''' The onboarding handler '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if session["onboarded"]:
        return redirect(url_for('home'))

    response = requests.get(f'https://{HOST}/api/v1/genres')
    if response.status_code == 200:
        genres = []
        for i in response.json():
            genres.append(response.json()[i]["data"])

    if request.method == 'POST':
        if int(request.form.get('done')) == 0:
            return render_template('onboarding.html',
                                   uuid=uuid4(), genres=genres,
                                   first_name=session["first_name"],
                                   last_name=session["last_name"],
                                   pic=session["user_pic"],
                                   error="Please select at least one genre.")

        else:
            headers = {'Content-Type': 'application/json'}
            json = {"onboarded": True}
            altered = requests.put('https://{}/api/v1/users/{}'
                                   .format(HOST, session["user_id"]),
                                   headers=headers, json=json)

            if altered.status_code == 200:
                session["onboarded"] = True
                return redirect(url_for('home'))

            else:
                return render_template('onboarding.html',
                                       uuid=uuid4(), genres=genres,
                                       first_name=session["first_name"],
                                       last_name=session["last_name"],
                                       pic=session["user_pic"],
                                       error=altered.json()["error"])

    return render_template('onboarding.html', uuid=uuid4(), genres=genres,
                           first_name=session["first_name"],
                           last_name=session["last_name"],
                           pic=session["user_pic"])
