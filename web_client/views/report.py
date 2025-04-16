#!/usr/bin/python3
''' The statistics page '''

from web_client.views import client_view
from flask import render_template, abort, session, redirect, url_for, request
from datetime import date
from calendar import month_name
from uuid import uuid4
import requests

from os import getenv
HOST = getenv('API_HOST')


def returner(**kwargs):
    ''' I'm avoiding the repition of things using this function '''

    return render_template('stats.html', uuid=uuid4(), pic=session["user_pic"],
                           name=session["first_name"], **kwargs)


def query(time: str, number: int, query_type: str):
    ''' The process of querying should be done once '''
    objects = {"Author", "Book", "Genre", "Review", "User"}

    if time == 'days':
        url = 'https://{}/api/v1/report/days/{}'.format(HOST, number)
        response = requests.get(url)

        if response.status_code == 200:
            stats = {i: response.json()[i] if query_type == 'stats' else
                     len(response.json()[i]) for i in objects}
            return dict(sorted(stats.items(), key=lambda item: item[0]))

    else:
        url = 'https://{}/api/v1/report/year/{}'
        year = number if time == 'year' else date.today().year

        if time != 'year' and number > 12 or number < 1:
            return returner(error="Invalid month")

        response = requests.get(url.format(HOST, year))

        if response.status_code == 200:

            if time == "month":
                month = number - 1
                stats = {i: response.json()[month][i] if query_type == 'stats'
                         else len(response.json()[month][i]) for i in objects}

                return dict(sorted(stats.items(), key=lambda item: item[0]))

            else:
                all = {i: [] if query_type == 'stats' else 0 for i in objects}
                all = dict(sorted(all.items(), key=lambda item: item[0]))

                for i in response.json():
                    for obj in objects:
                        all[obj] += (i[obj] if query_type == 'stats' else
                                     len(i[obj]))

                return all

        return returner(error=response.json()["error"])


@client_view.route('/statistics', methods=['GET', 'POST'],
                   strict_slashes=False)
def get_statistics():
    ''' This queries the api for new database material '''

    if not session or not session['logged'] or \
            session["user_type"] != 'librarian':
        abort(404)

    if request.method == "POST":
        if not request.form.get('number') or not request.form.get('time'):
            return returner(error="Please specify a duration")

        time = {request.form.get('time'): int(request.form.get('number'))}
        stats = query(list(time.keys())[0], list(time.values())[0], 'stats')

        return returner(stats=stats, **time,
                        month_name=month_name[list(time.values())[0]])

    return returner()


@client_view.route('/statistics/numbers', methods=['GET', 'POST'],
                   strict_slashes=False)
def get_statistics_numbers():
    ''' The all authors page  '''

    if not session or not session['logged'] or \
            session["user_type"] != 'librarian':
        abort(404)

    if request.method == "POST":
        if not request.form.get('number') or not request.form.get('time'):
            return returner(error="Please specify a duration")

        time = {request.form.get('time'): int(request.form.get('number'))}
        stats = query(list(time.keys())[0], list(time.values())[0], 'numbers')

        return returner(numbers=stats, **time,
                        month_name=month_name[list(time.values())[0]])

    return returner()
