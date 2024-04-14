#!/usr/bin/python3
''' The genres api handler '''
from api.v1.views import grand_view
from models import storage
from models.genre import Genre
from flask import jsonify, request, make_response, abort


@grand_view.route('/genres', methods=['GET'], strict_slashes=False)
def get_genres():
    ''' get all genres from the database '''

    genres = [i.to_dict() for i in storage.all(Genre).values()]
    return jsonify(genres) if len(genres) > 0 else abort(404)


@grand_view.route('/genres/<string:genre_id>', methods=['GET'], strict_slashes=False)
def get_genre(genre_id):
    ''' get a certain genre from the database '''

    genre = storage.get(Genre, genre_id)
    return jsonify(genre.to_dict()) if genre is not None else abort(404)


@grand_view.route('/genres', methods=['POST'], strict_slashes=False)
def create_genre():
    ''' creates a new genre in the database '''

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_genre = Genre(**request.get_json())
    new_genre.save()

    return make_response(jsonify(new_genre.to_dict()), 201)


@grand_view.route('/genres/<string:genre_id>', methods=['PUT'], strict_slashes=False)
def update_genre(genre_id):
    ''' creates a new genre in the database '''

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    genre = storage.get(Genre, genre_id)
    if genre is not None:
        genre.name = request.get_json()["name"]
        genre.save()
        return jsonify(genre.to_dict())

    abort(404)


@grand_view.route('/genres/<string:genre_id>', methods=['DELETE'], strict_slashes=False)
def delete_genre(genre_id):
    ''' creates a new genre in the database '''

    genre = storage.get(Genre, genre_id)
    if genre is not None:
        storage.delete(genre)
        storage.save()
        return jsonify({})

    abort(404)
