#!/usr/bin/python3
""" Index """
from models.author import Author
from models.book import Book
from models.book_author import BookAuthor
from models.book_genre import BookGenre
from models.genre import Genre
from models.review import Review
from models.user import User
from models import storage
from flask_api.v1.views import grand_view
from flask import jsonify


@grand_view.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@grand_view.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Author, Book, BookAuthor, BookGenre, Genre, Review, User]
    names = ["authors", "books", "book_authors", "book_genres",
     "genres", "reviews", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
