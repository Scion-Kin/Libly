#!/usr/bin/python3
''' This is the search algorithm for the web app '''
from models import storage
from models.author import Author
from models.book import Book
from models.book_author import BookAuthor
from models.book_genre import BookGenre
from models.genre import Genre
from models.user import User
from flask_api.v1.views import grand_view
from flask import request, jsonify


@grand_view.route('/search', methods=['POST'], strict_slashes=False)
def search():
    ''' This searches the whole database
    for anything containing the passed keywords '''

    keywords = list(request.get_json()["keywords"].split(' '))

    found = {
        "books": [],
        "authors": [],
        "genres": [],
        "users": []
    }

    for i in keywords:
        in_books = [j.to_dict() for j in storage.all(Book).values() if i in j.title.lower()]
        in_authors = [j.to_dict() for j in storage.all(Author).values() if i in j.first_name.lower() or i in j.last_name.lower()]
        in_genres = [j.to_dict() for j in storage.all(Genre).values() if i in j.name.lower()]
        in_users = [j.to_dict() for j in storage.all(User).values() if i in j.first_name.lower() or i in j.last_name.lower()]

        if len(in_books) > 0:
            for book in in_books:
                if len([i for i in found["books"] if i["id"] == book["id"]]) < 1:
                    found["books"].append(book) 

        if len(in_authors) > 0:
            for author in in_authors:
                if len([i for i in found["authors"] if i["id"] == author["id"]]) < 1:
                    found["authors"].append(author)

        if len(in_genres) > 0:
            for genre in in_genres:
                if len([i for i in found["genres"] if i["id"] == genre["id"]]) < 1:
                    found["genres"].append(genre)

        if len(in_users) > 0:
            for user in in_users:
                del user["password"]
                if len([i for i in found["users"] if i["id"] == user["id"]]) < 1:
                    found["users"].append(user)

    return jsonify(found)
