#!/usr/bin/python3
''' The genres api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.genre import Genre
from models.book import Book
from models.book_genre import BookGenre
from flask import jsonify, request, make_response, abort


@grand_view.route('/genres', methods=['GET'], strict_slashes=False)
def get_genres():
    ''' get all genres from the database '''

    all = [i.to_dict() for i in storage.all(Genre).values()]
    if len(all) == 0:
        abort(404)

    genres = {}
    for i in all:
        book_genres = [j for j in storage.all(BookGenre).values() if j.genre_id == i["id"]]
        genres[i["name"]] = {}
        genres[i["name"]]["_genre_id"] = i["id"]
        genres[i["name"]]["book_list"] = []
        if len(book_genres) > 0:
            for book_genre in book_genres:
                book = storage.get(Book, book_genre.book_id)
                genres[i["name"]]["book_list"].append(book.to_dict())

    return jsonify(genres) 


@grand_view.route('/genres/<string:genre_id>', methods=['GET'], strict_slashes=False)
def get_genre(genre_id):
    ''' get a certain genre from the database '''

    got = storage.get(Genre, genre_id)
    if not got:
        abort(404)
    genre = {}
    book_genres = [j for j in storage.all(BookGenre).values() if j.genre_id == genre_id]
    genre[got.name] = {}
    genre[got.name]["_genre_id"] = got.id
    genre[got.name]["book_list"] = []
    if len(book_genres) > 0:
        for book_genre in book_genres:
            book = storage.get(Book, book_genre.book_id)
            genre[got.name]["book_list"].append(book.to_dict())

    return jsonify(genre)


@grand_view.route('/genres', methods=['POST'], strict_slashes=False)
def create_genre():
    ''' creates a new genre in the database '''

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    genres = [i for i in storage.all(Genre).values() if i.name.lower() == request.get_json()["name"].lower()]
    if len(genres) > 0:
        return make_response(jsonify({"error": "genre exists"}), 403)

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
        all_book_rels = [i for i in storage.all(BookGenre).values() if i.genre_id == genre_id]
        all_book_ids = [i.book_id for i in all_book_rels]
        for i in all_book_ids:
            book = storage.get(Book, i)
            storage.delete(book)
            storage.save()

        for i in all_book_rels:
            storage.delete(i)
            storage.save()
        storage.delete(genre)
        storage.save()

        return jsonify({})

    abort(404)
