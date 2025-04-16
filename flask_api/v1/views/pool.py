#!/usr/bin/python3
''' This defines methods to be used in password resets '''

from flask_api.v1.views import grand_view
from flask import request, jsonify, make_response
from models import storage
from os import getenv
import MySQLdb
import random
import requests

def get_db():
    db = (MySQLdb.connect(host='localhost', user=getenv('MYSQL_USER', 'libly_user'),
          passwd=getenv('MYSQL_PASSWORD', 'libDev'), db=getenv('MYSQL_DB', 'libDev'),
          port=3306))

    return db, db.cursor()


@grand_view.route('/pool/<string:user_id>', methods=['POST'],
                  strict_slashes=False)
def verify_from_pool(user_id):
    ''' verify the reset code for a certain user '''

    if "reset_code" not in request.get_json():
        return make_response(jsonify({"error": "missing reset code"}), 400)

    db, cur = get_db()
    cur.execute('SELECT * FROM pool WHERE user_id = %s and code = %s',
                (user_id, request.get_json()["reset_code"]))
    rows = cur.fetchall()
    if len(rows) > 0:
        return jsonify({"success": "code verified"})

    db.close()
    return make_response(jsonify({"error": "code verification failed"}), 404)


@grand_view.route('/pool', methods=['POST'], strict_slashes=False)
def insert_into_pool():
    ''' insert a user into a password reset pool '''

    user = [i for i in storage.all('User').values()
            if i.email == request.get_json()["email"]]

    if len(user) == 0:
        return make_response(jsonify({"error": "User not found"}), 404)

    reset_code = random.randint(10000000, 99999999)
    db, cur = get_db()
    cur.execute('DELETE FROM pool WHERE user_id = %s', (user[0].id,))
    # parameters must be a tuple

    cur.execute('INSERT INTO pool VALUES (%s, %s)', (user[0].id, reset_code))
    db.commit()
    db.close()

    mail = requests.post('https://usernet.tech/mail/reset',
                         headers={"Content-Type": "application/json"},
                         json={"reset_code": reset_code,
                               "email": request.get_json()["email"],
                               "name": user[0].first_name})

    if mail.status_code != 200:
        return make_response(jsonify({"success": user[0].id}), 201)

    else:
        return make_response(jsonify({"error": "Could not send reset code. Try again later"}), 500)

@grand_view.route('/users/reset/<string:user_id>', methods=['PUT'],
                  strict_slashes=False)
def get_from_pool(user_id):
    ''' get the reset code for a certain user '''

    user = storage.get("User", user_id)

    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    if "new_password" not in request.get_json() or\
            "reset_code" not in request.get_json():

        return make_response(jsonify({"error":
                                      "missing reset code or password"}),
                             400)

    db, cur = get_db()
    cur.execute('SELECT * FROM pool WHERE user_id = %s and code = %s',
                (user.id, request.get_json()["reset_code"]))

    rows = cur.fetchall()
    try:
        if len(rows) > 0:
            user.password = request.get_json()["new_password"]
            user.save()

            cur.execute('DELETE FROM pool WHERE user_id = %s', (user.id, ))
            db.commit()

            return jsonify(user.to_dict())

        return make_response(jsonify({"error": "Wrong reset code"}), 403)

    except Exception as e:
        return make_response(jsonify({"error": f"{e}"}), 500)
    
    finally:
        db.close()
