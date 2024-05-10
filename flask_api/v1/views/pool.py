#!/usr/bin/python3
''' This defines methods to be used in password resets '''

from flask_api.v1.views import grand_view
from flask import request, abort, jsonify, make_response
from models import storage
import MySQLdb
import random
import requests


db = (MySQLdb.connect(host='localhost', user='libly_user',
      passwd='libDev', db='libly', port=3306))

cur = db.cursor()


@grand_view.route('/pool/<string:user_id>', methods=['POST'], strict_slashes=False)
def verify_from_pool(user_id):
    ''' verify the reset code for a certain user '''

    cur.execute('SELECT * FROM pool WHERE user_id = %s and code = %s',
                (user_id, request.get_json()["reset_code"]))
    rows = cur.fetchall()
    if len(rows) > 0:
        return jsonify({"success": "code verified"})

    return make_response(jsonify({"error": "code verification failed"}), 404)


@grand_view.route('/pool', methods=['POST'], strict_slashes=False)
def insert_into_pool():
    ''' insert a user into a password reset pool '''

    user = [i for i in storage.all('User').values() if i.email == request.get_json()["email"]]

    if len(user) == 0:
        return make_response(jsonify({"error": "User not found"}), 404)

    reset_code = random.randint(10000000, 99999999)
    cur.execute('DELETE FROM pool WHERE user_id = %s', (user[0].id,)) # parameters must be a tuple
    db.commit()

    cur.execute('INSERT INTO pool VALUES (%s, %s)', (user[0].id, reset_code))
    db.commit()

    mail = requests.post('https://usernet.tech/mail/reset',
                         headers={"Content-Type": "application/json"},
                         json={"reset_code": reset_code,
                               "email": request.get_json()["email"],
                               "name": user[0].first_name})

    return make_response(jsonify({"success": user[0].id}), 201)  # return the user's id


@grand_view.route('/users/reset/<string:user_id>', methods=['PUT'], strict_slashes=False)
def get_from_pool(user_id):
    ''' get the reset code for a certain user '''

    user = storage.get("User", user_id)

    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    cur.execute('SELECT * FROM pool WHERE user_id = %s and code = %s',
                (user.id, request.get_json()["reset_code"]))

    rows = cur.fetchall()
    if len(rows) > 0:
        user.password = request.get_json()["new_password"]
        user.save()

        cur.execute('DELETE FROM pool WHERE user_id = %s', (user.id, ))
        db.commit()

        return jsonify(user.to_dict())

    return make_response(jsonify({"error": "wrong reset code"}), 403)
