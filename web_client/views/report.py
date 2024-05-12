#!/usr/bin/python3
''' The statistics page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for, request
from datetime import date
from calendar import month_name
from uuid import uuid4
import requests


@client_view.route('/statistics', methods=['GET', 'POST'], strict_slashes=False)
def get_statistics():
    ''' This queries the api for new database material '''
    if session and session['logged'] == True:

        if session["user_type"] != 'librarian':
            abort(404)

        if request.method == "POST":
            if not request.form.get('number') or not request.form.get('time'):
                return render_template('stats.html', uuid=uuid4(),
                                       pic=session["user_pic"],
                                       name=session["first_name"], 
                                       error="Please specify a duration")

            time = request.form.get('time')
            if time == 'days':
                response = requests.get('https://usernet.tech/api/v1/report/days/{}'.
                                        format(int(request.form.get('number'))))

                if response.status_code == 200:
                    return render_template('stats.html', stats={
                                           "authors": response.json()["authors"],
                                           "books": response.json()["books"],
                                           "genres": response.json()["genres"],
                                           "reviews": response.json()["reviews"],
                                           "users": response.json()["users"]},
                                           uuid=uuid4(), pic=session["user_pic"], 
                                           name=session["first_name"], 
                                           days=(int(request.form.get('number'))))

            else:
                if time == "year":
                    response = requests.get('https://usernet.tech/api/v1/report/year/{}'.
                                            format(request.form.get('number')))
                else:
                    if int(request.form.get('number')) > 12 or int(request.form.get('number')) < 1:
                        return render_template('stats.html',
                                               pic=session["user_pic"], uuid=uuid4(),
                                               name=session["first_name"], error="Invalid month")

                    response = requests.get('https://usernet.tech/api/v1/report/year/{}'.
                                            format(date.today().year))

                if response.status_code == 200:

                    if time == "month":
                        month = int(request.form.get('number')) - 1
                        return render_template('stats.html', stats={
                                               "authors": response.json()[month]["authors"],
                                               "books": response.json()[month]["books"],
                                               "genres": response.json()[month]["genres"],
                                               "reviews": response.json()[month]["reviews"],
                                               "users": response.json()[month]["users"]}, uuid=uuid4(),
                                               pic=session["user_pic"], name=session["first_name"],
                                               month_name=month_name[month + 1], month=(month + 1))

                    else:
                        year = int(request.form.get('number'))
                        all = {"authors": [], "books": [], "genres": [], "reviews": [], "users": []}

                        for i in response.json():
                            all["authors"] += i["authors"]
                            all["books"] += i["books"]
                            all["genres"] += i["genres"]
                            all["reviews"] += i["reviews"]
                            all["users"] += i["users"]

                        return render_template('stats.html', stats=all, uuid=uuid4(),
                                               pic=session["user_pic"], name=session["first_name"],
                                               time=request.form.get('number'), year=(int(year)))

            return render_template('stats.html', uuid=uuid4(),
                                   pic=session["user_pic"],
                                   name=session["first_name"], error=response.json()["error"])

        return render_template('stats.html', uuid=uuid4(),
                                pic=session["user_pic"], name=session["first_name"])

    return redirect(url_for('home'))


@client_view.route('/statistics/numbers', methods=['GET', 'POST'], strict_slashes=False)
def get_statistics_numbers():
    ''' The all authors page  '''
    if session and session['logged'] == True:

        if session["user_type"] != 'librarian':
            abort(404)

        if request.method == "POST":
            if not request.form.get('number') or not request.form.get('time'):
                return render_template('stats.html', uuid=uuid4(),
                                       pic=session["user_pic"],
                                       name=session["first_name"], 
                                       error="Please specify a duration")

            time = request.form.get('time')
            if time == 'days':
                response = requests.get('https://usernet.tech/api/v1/report/days/{}'.
                                        format(int(request.form.get('number'))))

                if response.status_code == 200:
                    return render_template('stats.html', numbers={
                                           "authors": len(response.json()["authors"]),
                                           "books": len(response.json()["books"]),
                                           "genres": len(response.json()["genres"]),
                                           "reviews": len(response.json()["reviews"]),
                                           "users": len(response.json()["users"])},
                                           uuid=uuid4(), pic=session["user_pic"], 
                                           name=session["first_name"], 
                                           days=(int(request.form.get('number'))))

            else:
                if time == "year":
                    response = requests.get('https://usernet.tech/api/v1/report/year/{}'.
                                            format(request.form.get('number')))
                else:
                    if int(request.form.get('number')) > 12 or int(request.form.get('number')) < 1:
                        return render_template('stats.html',
                                               pic=session["user_pic"], uuid=uuid4(),
                                               name=session["first_name"], error="Invalid month")
                    response = requests.get('https://usernet.tech/api/v1/report/year/{}'.
                                            format(date.today().year))

                if response.status_code == 200:

                    if time == "month":
                        month = int(request.form.get('number')) - 1
                        return render_template('stats.html', numbers={
                                               "authors": len(response.json()[month]["authors"]),
                                               "books": len(response.json()[month]["books"]),
                                               "genres": len(response.json()[month]["genres"]),
                                               "reviews": len(response.json()[month]["reviews"]),
                                               "users": len(response.json()[month]["users"])},
                                               uuid=uuid4(),
                                               pic=session["user_pic"], name=session["first_name"],
                                               month_name=month_name[month + 1], month=(month + 1))

                    else:
                        year = int(request.form.get('number'))
                        numbers = {"authors": 0, "books": 0, "genres": 0, "reviews": 0, "users": 0}

                        for i in response.json():
                            numbers["authors"] += len(i["authors"])
                            numbers["books"] += len(i["books"])
                            numbers["genres"] += len(i["genres"])
                            numbers["reviews"] += len(i["reviews"])
                            numbers["users"] += len(i["users"])

                        return render_template('stats.html',
                                               numbers=numbers, uuid=uuid4(),
                                               pic=session["user_pic"], name=session["first_name"],
                                               time=request.form.get('number'), year=(int(year)))

            return render_template('stats.html', uuid=uuid4(),
                                   pic=session["user_pic"],
                                   name=session["first_name"], error=response.json()["error"])

        return render_template('stats.html', uuid=uuid4(),
                                pic=session["user_pic"], name=session["first_name"])

    return redirect(url_for('home'))
