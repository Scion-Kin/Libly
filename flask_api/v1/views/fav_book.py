#!/usr/bin/python3
''' The books api handler for favoriting '''
from flask_api.v1.views import grand_view
from models import storage
from models.favorite_book import FavoriteBook
from models.user import User
from flask import jsonify, abort, request, make_response


@grand_view.route('/favs/books', methods=['GET'], strict_slashes=False)
def get_fav_books():
    ''' get all favorite instances from the database '''

    all = [i.to_dict() for i in storage.all(FavoriteBook).values()]

    return jsonify(all) if len(all) > 0 else abort(404)


@grand_view.route('/<string:user_id>/favs/books', methods=['GET'], strict_slashes=False)
def get_user_fav_books(user_id):
    ''' get all favorite instances from the database by a certain user '''

    favs = [i.to_dict() for i in storage.all(FavoriteBook).values() if i.user_id == user_id]
    return jsonify(favs) if len(favs) > 0 else abort(404)


@grand_view.route('/favs/books', methods=['POST'], strict_slashes=False)
def create_book_fav():
    ''' creates a new favorite in the database '''

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user id"}), 400)

    if "book_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing book id"}), 400)

    user = storage.get('User', request.get_json()["user_id"])
    book = storage.get('Book', request.get_json()["book_id"])

    if not user or not book:
        abort(404)

    all = [i for i in storage.all(FavoriteBook).values() if
           i.user_id == request.get_json()["user_id"] and
           i.book_id == request.get_json()["book_id"]]

    if len(all) > 0:
        return make_response(jsonify({"error": "Already favorited"}), 403)

    new_fav = FavoriteBook(user_id=request.get_json()["user_id"], book_id=request.get_json()["book_id"])
    new_fav.save()

    return make_response(jsonify(new_fav.to_dict()), 201)


@grand_view.route('/favs/books/<string:fav_id>', methods=['DELETE'], strict_slashes=False)
def delete_book_fav(fav_id):
    ''' creates a favorite instance from the database '''

    fav = storage.get(FavoriteBook, fav_id)
    if fav is not None:
        storage.delete(fav)
        storage.save()
        return jsonify({})

    abort(404)
