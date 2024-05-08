#!/usr/bin/python3
''' Defines a route for user onboarding '''

from web_client.views import client_view
from flask import render_template, session, request, redirect, url_for, jsonify
from uuid import uuid4
import requests

@client_view.route('/onboarding', methods=['GET', 'POST'], strict_slashes=False)
def onboarding():
    ''' The onboarding handler '''

    if not session or session["logged"] != True:
        return redirect(url_for('home'))

    response = requests.get('https://usernet.tech/api/v1/genres')
    if response.status_code == 200:
        genres = []
        for i in response.json():
            genres.append(response.json()[i]["data"])

    if request.method == 'POST':
        
        if int(request.form.get('done')) == 0:
            return render_template('onboarding.html', uuid=uuid4(), genres=genres,
                                first_name=session["first_name"], last_name=session["last_name"],
                                pic=session["user_pic"], error="Please select at least one genre.")

        else:
            altered = requests.put('https://usernet.tech/api/v1/users/{}'.format(session["user_id"]), 
                                   headers={'Content-Type': 'application/json'}, json=jsonify({"onboarded": True}))

            if altered.status_code == 200:
                session["onboarded"] = True
                return redirect(url_for('home'))

            else:
                return render_template('onboarding.html', uuid=uuid4(), genres=genres,
                                       first_name=session["first_name"], last_name=session["last_name"],
                                       pic=session["user_pic"], error=altered.json()["error"])

    return render_template('onboarding.html', uuid=uuid4(), genres=genres,
                           first_name=session["first_name"], last_name=session["last_name"],
                           pic=session["user_pic"])
