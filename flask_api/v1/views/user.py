#!/usr/bin/python3
''' The users api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.user import User
from models.review import Review
from flask import jsonify, abort, make_response, request
import os


@grand_view.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    ''' get all users from the database '''

    all = [i.to_dict() for i in storage.all(User).values()]

    if len(all) == 0:
        abort(404)

    for i in all:
        del i["password"]

    users = {}
    for i in all:
        name = i["first_name"] + ' ' + i["last_name"]
        users[name] = {}
        users[name]["data"] = i

    return jsonify(users)


@grand_view.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    ''' get a certain user from the database '''

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    del user.password

    users = {}
    name = user.first_name + ' ' + user.last_name
    users[name] = {}
    users[name]["data"] = user.to_dict()
    return jsonify(users)


@grand_view.route('/users/<string:user_id>/reviews', methods=['GET'], strict_slashes=False)
def get_user_reviews(user_id):
    ''' get reviews made by a certain user from the database '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    all_reviews = [i.to_dict() for i in storage.all(Review).values() if i.user_id == user_id]
    return jsonify(all_reviews) if len(all_reviews) > 0 else abort(404)


@grand_view.route('/users/confirm/<string:user_id>', strict_slashes=False)
def activate(user_id):
    ''' activate the user's account '''

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if user.confirmed == True:
        return make_response(jsonify({"error": "account already activated"}), 409)

    else:
        user.confirmed = True
        user.save()

    return jsonify({"success": "user activated"})


@grand_view.route('/login', methods=['POST'], strict_slashes=False)
def login():
    ''' log in the user '''

    all = [i for i in storage.all(User).values() if i.email == request.get_json()["email"]]

    if len(all) < 0:
        return make_response(jsonify({"error": "User not found"}), 401)

    if all[0].confirmed != True:
        return make_response(jsonify({"error": "You have not confirmed your email. Please check your email inbox and activate your account"}), 401)

    if all[0].password == request.get_json()["password"]:
        return jsonify({"user": all[0].to_dict()})

    return make_response(jsonify({"error": "Wrong password"}), 401)


@grand_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    ''' creates a new user in the database '''

    if "email" not in request.get_json() or "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing credential(s)"}), 400)

    all_users = [i for i in storage.all(User).values() if i.email == request.get_json()["email"]]
    if len(all_users) > 0:
        return make_response(jsonify({"error": "email already exists"}), 400)

    new_user = User(**request.get_json())
    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@grand_view.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' creates a new user in the database '''

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "onboarded" in request.get_json():  
        try:
            user.onboarded = bool(request.get_json()["onboarded"])
            user.save()
            return jsonify(user.to_dict())

        except ValueError:
            return make_response(jsonify({"error": "onboarded value must be boolean"}), 400)

    else:

        if "adminPassword" in request.get_json() or "password" in request.get_json():
            admins = []
            if "adminPassword" in request.get_json():
                admins = [i for i in storage.all(User).values() if
                        i.user_type == "librarian" and 
                        i.password == request.get_json()["adminPassword"]]

            ignore = ['id', 'created_at', 'updated_at']
            if len(admins) > 0 or (request.get_json()["password"] and user.password == request.get_json()["password"]):
                for key, value in request.get_json().items():
                    if key not in ignore:
                        setattr(user, key, value)
                if "new_password" in request.get_json():
                    user.password = request.get_json()["new_password"]
                user.save()
                return jsonify(user.to_dict())
            else:
                return make_response(jsonify({"error": "incorrect or missing password"}), 401)

        return make_response(jsonify({"error": "unauthorized"}), 401)


@grand_view.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    ''' creates a new user in the database '''

    user = storage.get(User, user_id)
    admins = [i for i in storage.all(User).values() if i.user_type == "librarian"]
    admins = [i.password for i in admins]

    if user is not None:
        if request.get_json()["password"] and user.password == request.get_json()["password"] or\
        request.get_json()["password"] in admins:

            try:
                if user.pic != 'user-avatar.jpg':
                    os.remove('web_client/static/images/' + user.pic)

            except FileNotFoundError:
                pass

            storage.delete(user)
            storage.save()
            return jsonify({})
        else:
            return make_response(jsonify({"error": "incorrect or missing password"}), 401)

    abort(404)
