#!/usr/bin/python3
''' The genres api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.favorite_genre import FavoriteGenre
from models.user import User
from flask import jsonify, abort, request, make_response


@grand_view.route('/favs/genres', methods=['GET'], strict_slashes=False)
def get_fav_genres():
    ''' get all favorite instances from the database '''

    all = [i.to_dict() for i in storage.all(FavoriteGenre).values()]

    return jsonify(all) if len(all) > 0 else abort(404)


@grand_view.route('/<string:user_id>/favs/genres', methods=['GET'], strict_slashes=False)
def get_user_fav_genres(user_id):
    ''' get all favorite instances from the database by a certain user '''

    favs = [i.to_dict() for i in storage.all(FavoriteGenre).values() if i.user_id == user_id]
    return jsonify(favs) if len(favs) > 0 else abort(404)


@grand_view.route('/favs/genres', methods=['POST'], strict_slashes=False)
def create_genre_fav():
    ''' creates a new favorite in the database '''

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user id"}), 400)

    if "genre_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing genre id"}), 400)

    user = storage.get('User', request.get_json()["user_id"])
    genre = storage.get('Genre', request.get_json()["genre_id"])

    if not user or not genre:
        abort(404)

    all = [i for i in storage.all(FavoriteGenre) if i.user_id == request.get_json()["user_id"] and i.genre_id == request.get_json()["genre_id"]]

    if len(all) > 0:
        return make_response(jsonify({"error": "Already favorited"}), 403)

    new_fav = FavoriteGenre(user_id=request.get_json()["user_id"], genre_id=request.get_json()["genre_id"])
    new_fav.save()

    return make_response(jsonify(new_fav.to_dict()), 201)


@grand_view.route('/favs/genres/<string:fav_id>', methods=['DELETE'], strict_slashes=False)
def delete_genre_fav(fav_id):
    ''' creates a favorite instance from the database '''

    fav = storage.get(FavoriteGenre, fav_id)
    if fav is not None:
        storage.delete(fav)
        storage.save()
        return jsonify({})

    abort(404)
