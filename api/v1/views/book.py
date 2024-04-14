#!/usr/bin/python3
''' The books api handler '''
from api.v1.views import grand_view
from models import storage
from models.book import Book
from models.book_author import BookAuthor
from models.book_genre import BookGenre
from flask import jsonify


@grand_view.route('/books/<string:book_id>', methods=['GET'], strict_slashes=False)
def get_books(book_id):
    ''' get books from the database '''

    if not book_id:
        books = [i.to_dict() for i in storage.all(Book).values()]

        return jsonify(books)

    books = [i.to_dict() for i in storage.all(Book).values() if i.id == book_id]
    return jsonify(books[0])
