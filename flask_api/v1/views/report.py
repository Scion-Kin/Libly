#!/usr/bin/python3
''' The authors api handler '''
from flask_api.v1.views import grand_view
from models import storage
from flask import jsonify, make_response, request
from datetime import datetime, timedelta


@grand_view.route('/report/days/<int:days>', strict_slashes=False)
def get_report(days):
    ''' get all authors from the database '''

    period = datetime.now() - timedelta(days=days)
    full = [i.to_dict() for i in storage.all().values() if
            i.created_at >= period]

    obs = {"Author", "Book", "Genre", "Review", "User"}
    report = {i: [j for j in full if j["__class__"] == i] for i in obs}

    return jsonify(dict(sorted(report.items(), key=lambda item: item[0])))


@grand_view.route('/report/year/<int:year>', strict_slashes=False)
def year_report(year):
    ''' Gets the report of a certain year '''
    if year < 2024 or year > datetime.now().year:
        return make_response(jsonify({"error": "Invalid year given"}), 400)

    full = [i for i in storage.all().values() if i.created_at.year == year]
    all_months = []

    # get data from all months
    for i in range(1, 13):
        month = [j.to_dict() for j in full if j.created_at.month == i]
        obs = {"Author", "Book", "Genre", "Review", "User"}
        report = {k: [j for j in month if j["__class__"] == k] for k in obs}

        all_months.append(dict(sorted(report.items(),
                                      key=lambda item: item[0])))

    return jsonify(all_months)
