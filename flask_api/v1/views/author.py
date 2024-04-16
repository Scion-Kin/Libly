#!/usr/bin/python3
''' The authors api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.author import Author
from models.book import Book
from models.book_author import BookAuthor
from flask import jsonify, request, make_response, abort


@grand_view.route('/authors', methods=['GET'], strict_slashes=False)
def get_authors():
    ''' get all authors from the database '''

    all = [i.to_dict() for i in storage.all(Author).values()]
    if len(all) == 0:
        abort(404)

    authors = {}
    for i in all:
        book_authors = [j for j in storage.all(BookAuthor).values() if j.author_id == i["id"]]
        name = (i["first_name"] + ' ' + i["middle_name"] + ' ' + i["last_name"]) if\
            i["middle_name"] is not None else (i["first_name"] + ' ' + i["last_name"])

        authors[name] = {}
        authors[name]["_author_id"] = i["id"]
        authors[name]["book_list"] = []
        if len(book_authors) > 0:
            for book_author in book_authors:
                book = storage.get(Book, book_author.book_id)
                authors[name]["book_list"].append(book.to_dict())

    return jsonify(authors) 


@grand_view.route('/authors/<string:author_id>', methods=['GET'], strict_slashes=False)
def get_author(author_id):
    ''' get a certain author from the database '''

    got = storage.get(Author, author_id)
    if not got:
        abort(404)
    author = {}
    book_authors = [j for j in storage.all(BookAuthor).values() if j.author_id == author_id]
    name = (got.first_name + ' ' + got.middle_name + ' ' + got.last_name) if\
            got.middle_name is not None else (got.first_name + ' ' + got.last_name)

    author[name] = {}
    author[name]["_author_id"] = got.id
    author[name]["book_list"] = []
    if len(book_authors) > 0:
        for book_author in book_authors:
            book = storage.get(Book, book_author.book_id)
            author[name]["book_list"].append(book.to_dict())

    return jsonify(author)


@grand_view.route('/authors', methods=['POST'], strict_slashes=False)
def create_author():
    ''' creates a new author in the database '''

    if "first_name" not in request.get_json() or "last_name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name(s)"}), 400)

    authors = [i for i in storage.all(Author).values() if
               i.first_name.lower() == request.get_json()["first_name"].lower() and
               i.last_name.lower() == request.get_json()["last_name"].lower()]

    try:
        middle_name = request.get_json()["middle_name"]
        middle_name = middle_name.lower() if middle_name is not None else None
        if len(authors) > 0 and authors[0].middle_name.lower() == middle_name:
            return make_response(jsonify({"error": "author exists"}), 403)

    except KeyError:
        if len(authors) > 0:
            return make_response(jsonify({"error": "author exists"}), 403)

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
        all_book_rels = [i for i in storage.all(BookAuthor).values() if i.author_id == author_id]
        all_book_ids = [i.book_id for i in all_book_rels]
        for i in all_book_ids:
            book = storage.get(Book, i)
            storage.delete(book)
            storage.save()

        for i in all_book_rels:
            storage.delete(i)
            storage.save()
        storage.delete(author)
        storage.save()

        return jsonify({})

    abort(404)
