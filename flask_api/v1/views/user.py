#!/usr/bin/python3
''' The users api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.user import User
from models.review import Review
from flask import jsonify, abort, make_response, request


@grand_view.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    ''' get all users from the database '''

    users = [i.to_dict() for i in storage.all(User).values()]

    if len(users) == 0:
        abort(404)

    for i in users:
        del i["password"]

    return jsonify(users)


@grand_view.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    ''' get a certain user from the database '''

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    del user.password
    return jsonify(user.to_dict()) 


@grand_view.route('/users/<string:user_id>/reviews', methods=['GET'], strict_slashes=False)
def get_user_reviews(user_id):
    ''' get reviews made by a certain user from the database '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    all_reviews = [i.to_dict() for i in storage.all(Review).values() if i.user_id == user_id]
    return jsonify(all_reviews) if len(all_reviews) > 0 else abort(404)


@grand_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    ''' creates a new user in the database '''

    if "email" not in request.get_json() or "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing credential(s)"}), 400)

    if "user_type" in request.get_json():
        admin = [i for i in storage.all(User).values() if i.user_type == "king"]
        if "sign_password" in request.get_json() and request.get_json()["sign_password"] == admin[0].password:
            new_user = User(**request.get_json())
            new_user.user_type = 'king'
            new_user.save()
        else:
            return make_response(jsonify({"error": "authentication failed"}), 403)

    else:
        new_user = User(**request.get_json())
        new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@grand_view.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' creates a new user in the database '''

    user = storage.get(User, user_id)
    if user is not None:
        ignore = ['id', 'created_at', 'updated_at']
        if request.get_json()["password"] and user.password == request.get_json()["password"]:
            for key, value in request.get_json().items():
                if key not in ignore:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict())
        else:
            return make_response(jsonify({"error": "incorrect or missing password"}), 401)

    abort(404)


@grand_view.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    ''' creates a new user in the database '''

    user = storage.get(User, user_id)
    if user is not None:
        if request.get_json()["password"] and user.password == request.get_json()["password"]:
            storage.delete(user)
            storage.save()
            return jsonify({})
        else:
            return make_response(jsonify({"error": "incorrect or missing password"}), 401)

    abort(404)