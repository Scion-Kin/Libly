#!/usr/bin/python3
''' The users api handler '''
from api.v1.views import grand_view
from models import storage
from models.user import User
from flask import jsonify


@grand_view.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    ''' get all users from the database '''

    users = [i.to_dict() for i in storage.all(User).values()]
    return jsonify(users)


@grand_view.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    ''' get a certain user from the database '''

    user = [i.to_dict() for i in storage.all(User).values() if i.id == user_id]
    return jsonify(user[0])
