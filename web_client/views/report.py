#!/usr/bin/python3
''' The statistics page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for, request
from datetime import date
from calendar import month_name
from uuid import uuid4
import requests


def returner(**kwargs):
    ''' I'm avoiding the repition of things using this function '''

    return render_template('stats.html', uuid=uuid4(), pic=session["user_pic"],
                           name=session["first_name"], **kwargs)


@client_view.route('/statistics', methods=['GET', 'POST'],
                   strict_slashes=False)
def get_statistics():
    ''' This queries the api for new database material '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if session["user_type"] != 'librarian':
        abort(404)

    if request.method == "POST":
        if not request.form.get('number') or not request.form.get('time'):
            return returner(error="Please specify a duration")

        time = request.form.get('time')
        number = int(request.form.get('number'))
        objects = {"authors", "books", "genres", "reviews", "users"}

        if time == 'days':
            url = 'https://usernet.tech/api/v1/report/days/{}'
            response = requests.get(url.format(number))

            if response.status_code == 200:
                stats = {i: response.json()[i] for i in objects}
                return returner(stats=stats, days=number)

        else:
            url = 'https://usernet.tech/api/v1/report/year/{}'
            if time == "year":
                response = requests.get(url.format(number))
            else:
                if number > 12 or number < 1:

                    return returner(error="Invalid month")

                response = requests.get(url.format(date.today().year))

            if response.status_code == 200:

                if time == "month":
                    month = number - 1
                    stats = {i: response.json()[month][i] for i in objects}

                    return returner(stats=stats, month=(month + 1),
                                    month_name=month_name[month + 1])

                else:
                    all = {i: [] for i in objects}

                    for i in response.json():
                        for obj in objects:
                            all[obj] += i[obj]

                    return returner(stats=all, year=(number),
                                    time=request.form.get('number'))

        return returner(error=response.json()["error"])

    return returner()


@client_view.route('/statistics/numbers', methods=['GET', 'POST'],
                   strict_slashes=False)
def get_statistics_numbers():
    ''' The all authors page  '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    if session["user_type"] != 'librarian':
        abort(404)

    if request.method == "POST":
        if not request.form.get('number') or not request.form.get('time'):
            return returner(error="Please specify a duration")

        time = request.form.get('time')
        number = int(request.form.get('number'))
        objects = {"authors", "books", "genres", "reviews", "users"}

        if time == 'days':
            url = 'https://usernet.tech/api/v1/report/days/{}'
            response = requests.get(url.format(number))

            if response.status_code == 200:
                numbers = {i: len(response.json()[i]) for i in objects}

                return returner(numbers=numbers, days=number)

        else:
            url = 'https://usernet.tech/api/v1/report/year/{}'

            if time == "year":
                response = requests.get(url.format(number))
            else:
                if number > 12 or number < 1:
                    return returner(error="Invalid month")
                response = requests.get(url.format(date.today().year))

            if response.status_code == 200:

                if time == "month":
                    month = number - 1
                    nums = {i: len(response.json()[month][i]) for i in objects}

                    return returner(numbers=nums, month=(month + 1),
                                    month_name=month_name[month + 1])

                else:
                    numbers = {i: 0 for i in objects}

                    for i in response.json():
                        for obj in objects:
                            numbers[obj] += len(i[obj])

                    return returner(numbers=numbers, year=(number),
                                    time=number)

        return returner(error=response.json()["error"])

    return returner()
