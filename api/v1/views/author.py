#!/usr/bin/python3
''' The authors api handler '''
from api.v1.views import grand_view
from models import storage
from models.author import Author
from flask import jsonify, request, make_response, abort


@grand_view.route('/authors', methods=['GET'], strict_slashes=False)
def get_authors():
    ''' get all authors from the database '''

    authors = [i.to_dict() for i in storage.all(Author).values()]
    return jsonify(authors) if len(authors) > 0 else abort(404)


@grand_view.route('/authors/<string:author_id>', methods=['GET'], strict_slashes=False)
def get_author(author_id):
    ''' get a certain author from the database '''

    author = storage.get(Author, author_id)
    return jsonify(author.to_dict()) if author is not None else abort(404)


@grand_view.route('/authors', methods=['POST'], strict_slashes=False)
def create_author():
    ''' creates a new author in the database '''

    if "first_name" not in request.get_json() or "last_name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name(s)"}), 400)

    new_author = Author(**request.get_json())
    new_author.save()

    return make_response(jsonify(new_author.to_dict()), 201)


@grand_view.route('/authors/<string:author_id>', methods=['PUT'], strict_slashes=False)
def update_author(author_id):
    ''' alters an author info in the database '''

    author = storage.get(Author, author_id)
    if author is not None:
        ignore = ['id', 'created_at', 'updated_at']

        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(author, key, value)

        author.save()
        return jsonify(author.to_dict())

    abort(404)


@grand_view.route('/authors/<string:author_id>', methods=['DELETE'], strict_slashes=False)
def delete_author(author_id):
    ''' creates a new author in the database '''

    author = storage.get(Author, author_id)
    if author is not None:
        storage.delete(author)
        storage.save()
        return jsonify({})

    abort(404)
