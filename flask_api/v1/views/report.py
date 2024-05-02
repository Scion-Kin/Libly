#!/usr/bin/python3
''' The authors api handler '''
from flask_api.v1.views import grand_view
from models import storage
from flask import jsonify, make_response, request
from datetime import date


@grand_view.route('/report/days/<int:days>', strict_slashes=False)
def get_report(days):
    ''' get all authors from the database '''

    if days > 30:
        return make_response(jsonify({"error": "Can't select more than 30 days"}), 400)

    today = str(date.today()).split('-')

    # here I add thirty days, in the case that the current date number is less than days requested.
    period = int(today[2]) - days
    period = period + 30 if period < 0 else period

    # get all items from this year
    all = [i for i in storage.all().values() if str(i.created_at).split(' ')[0].split('-')[0] == today[0]]

    if days > int(today[2]):
        # get all items from the requested range of days from last month
        if today[1] == '01':
            prev_month = [i.to_dict() for i in all if
                          str(i.created_at).split(' ')[0].split('-')[1] ==
                          '12' and str(i.created_at).split(' ')[0].split('-')[2] >= period]
        else:
            prev_month = [i.to_dict() for i in all if
                          int(str(i.created_at).split(' ')[0].split('-')[1]) ==
                          (int(today[1]) - 1) and int(str(i.created_at).split(' ')[0].split('-')[2]) >= period]

        # get all items from this month
        this_month = [i.to_dict() for i in all if str(i.created_at).split(' ')[0].split('-')[1] == today[1]]

        # combine last month to this month
        all = prev_month + this_month

    else:
        # get all items from this month
        all = [i for i in all if str(i.created_at).split(' ')[0].split('-')[1] == today[1]]

        # get all items from the requested range of days
        all = [i.to_dict() for i in all if period < int(str(i.created_at).split(' ')[0].split('-')[2])]

    all = {"authors": [i for i in all if i["__class__"] == "Author"],
           "books": [i for i in all if i["__class__"] == "Book"],
           "genres": [i for i in all if i["__class__"] == "Genre"],
           "reviews": [i for i in all if i["__class__"] == "Review"],
           "users": [i for i in all if i["__class__"] == "User"]}

    return jsonify(all)


@grand_view.route('/report/year/<int:year>', strict_slashes=False)
def year_report(year):
    ''' Gets the report of a certain year '''
    if year < 2024 or year > int(str(date.today()).split('-')[0]):
        return make_response(jsonify({"error": "Invalid year given"}), 400)

    all = [i for i in storage.all().values() if int(str(i.created_at).split(' ')[0].split('-')[0]) == year]

    all_months = []

    # get data from all months
    for i in range(1, 13):
        month = [j.to_dict() for j in all if int(str(j.created_at).split(' ')[0].split('-')[1]) == i]
        month = {"authors": [j for j in month if j["__class__"] == "Author"],
                 "books": [j for j in month if j["__class__"] == "Book"],
                 "genres": [j for j in month if j["__class__"] == "Genre"],
                 "reviews": [j for j in month if j["__class__"] == "Review"],
                 "users": [j for j in month if j["__class__"] == "User"]}

        all_months.append(month)
    return jsonify(all_months)
