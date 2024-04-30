#!/usr/bin/python3
''' The authors api handler '''
from flask_api.v1.views import grand_view
from models import storage
from flask import jsonify, make_response
from datetime import date


@grand_view.route('/report/<int:days>', strict_slashes=False)
def get_report(days):
    ''' get all authors from the database '''

    if days > 30:
        return make_response(jsonify({"error": "Can't view past 30 days"}), 400)

    today = str(date.today()).split('-')

    # get all items from this year
    all = [i for i in storage.all().values() if str(i.created_at).split(' ')[0].split('-')[0] == today[0]]

    # get all items from this month
    all = [i for i in all if str(i.created_at).split(' ')[0].split('-')[1] == today[1]]

    # get all items from the last seven days
    all = [i.to_dict() for i in all if int(today[2]) - days < int(str(i.created_at).split(' ')[0].split('-')[2])]
    all = { "authors": [i for i in all if i["__class__"] == "Author"],
            "books": [i for i in all if i["__class__"] == "Book"],
            "genres": [i for i in all if i["__class__"] == "Genre"],
            "reviews": [i for i in all if i["__class__"] == "Review"],
            "users": [i for i in all if i["__class__"] == "User"] }

    return jsonify(all)
