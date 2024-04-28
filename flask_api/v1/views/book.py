#!/usr/bin/python3
''' The books api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.book import Book
from models.author import Author
from models.genre import Genre
from models.book_author import BookAuthor
from models.book_genre import BookGenre
from flask import jsonify, request, make_response, abort
import os


@grand_view.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
    ''' get all books from the database '''

    all = [i.to_dict() for i in storage.all(Book).values()]
    if len(all) == 0:
        abort(404)

    books = {}
    for i in all:
        books[i["title"]] = {}
        books[i["title"]]["data"] = i

    return jsonify(books)


@grand_view.route('/books/<string:book_id>', methods=['GET'], strict_slashes=False)
def get_book(book_id):
    ''' get a certain book from the database '''
    book = storage.get(Book, book_id)
    books = {}
    books[book.title] = {}
    books[book.title]["data"] = book.to_dict()
    return jsonify(books)


@grand_view.route('/books', methods=['POST'], strict_slashes=False)
def create_book():
    ''' create a certain book from the database '''

    if "title" not in request.get_json() or "ISBN" not in request.get_json():
        return make_response(jsonify({"error": "Missing title or ISBN"}), 400)

    if "genres" not in request.get_json() or len(request.get_json()["genres"]) < 1:
        return make_response(jsonify({"error": "Missing genre(s)"}), 400)

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "unauthorized"}, 401))

    admins = [i for i in storage.all("User").values() if i.user_type == 'librarian' and i.password == request.get_json()["password"]]

    if len(admins) == 0:
        return make_response(jsonify({"error": "unauthorized"}, 401))

    new_book = Book(title=request.get_json()["title"],
                    ISBN=request.get_json()["ISBN"],
                    file_name=request.get_json()["file_name"],
                    pic=request.get_json()["pic"],
                    description=request.get_json()["description"])
    new_book.save()

    # Let's make a book and authors relationship

    if "authors" in request.get_json() and len(request.get_json()["authors"]) > 0:
        for i in request.get_json()["authors"]:
            author = storage.get(Author, i)
            if not author:
                all_rels = [i for i in storage.all(BookAuthor).values() if i.book_id == new_book.id]
                if len(all_rels) > 0:
                    for i in all_rels:
                        storage.delete(i)
                        storage.save()

                storage.delete(new_book)
                storage.save()

                try:
                    os.remove('web_client/books/' + new_book.file_name)

                except FileNotFoundError:
                    pass

                return make_response(jsonify({"error": "author not found"}), 404)

            new_author_rel = BookAuthor(book_id=new_book.id, author_id=i)
            new_author_rel.save()

    else:
        default_author = [i for i in storage.all(Author).values() if i.first_name == "Unknown"]
        if len(default_author) < 1:
            default_author = Author(first_name="Unknown", last_name="Unknown")
            default_author.save()
        else:
            default_author = default_author[0]
        new_author_rel = BookAuthor(book_id=new_book.id, author_id=default_author.id)
        new_author_rel.save()

    # Now let's make a book and genres relationship

    for i in request.get_json()["genres"]:
        genre = storage.get(Genre, i)
        if not genre:
            all_rels = [i for i in storage.all(BookGenre).values() if i.book_id == new_book.id]
            if len(all_rels) > 0:
                for i in all_rels:
                    storage.delete(i)
                    storage.save()

            all_rels = [i for i in storage.all(BookAuthor).values() if i.book_id == new_book.id]

            # No length check since if the loop got function got here, there is definitely a book authors relationship
            for i in all_rels: 
                storage.delete(i)
                storage.save()

            storage.delete(new_book)
            storage.save()

            try:
                os.remove('web_client/books/' + new_book.file_name)

            except FileNotFoundError:
                pass

            return make_response(jsonify({"error": "genre not found"}), 404)

        new_genre_rel = BookGenre(book_id=new_book.id, genre_id=i)
        new_genre_rel.save()

    return jsonify(new_book.to_dict())


@grand_view.route('/books/<string:book_id>', methods=['PUT'], strict_slashes=False)
def update_book(book_id):
    ''' alter info about a certain book from the database '''

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "unauthorized"}, 401))

    admins = [i for i in storage.all("User").values() if i.user_type == 'librarian' and i.password == request.get_json()["password"]]

    if len(admins) == 0:
        return make_response(jsonify({"error": "unauthorized"}, 401))

    book = storage.get(Book, book_id)
    if not book:
        abort(404)

    ignore = ['created_at', 'updated_at', 'id', '__class__']

    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(book, key, value)

    book.save()
    return jsonify(book.to_dict())

@grand_view.route('/books/<string:book_id>', methods=['DELETE'], strict_slashes=False)
def delete_book(book_id):
    ''' alter info about a certain book from the database '''

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "unauthorized"}, 401))

    admins = [i for i in storage.all("User").values() if i.user_type == 'librarian' and i.password == request.get_json()["password"]]

    if len(admins) == 0:
        return make_response(jsonify({"error": "unauthorized"}, 401))

    book = storage.get(Book, book_id)
    if not book:
        abort(404)

    try:
        os.remove('web_client/books/' + book.file_name)

    except FileNotFoundError:
        pass

    storage.delete(book)
    storage.save()

    return jsonify({"success": "book deleted"})
