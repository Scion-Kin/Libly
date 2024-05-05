#!/usr/bin/python3
''' The authors api handler '''
from flask_api.v1.views import grand_view
from models import storage
from flask import jsonify, make_response


@grand_view.route('/hot/<string:user_id>', strict_slashes=False)
def hot_list(user_id):
    ''' get all authors from the database '''

    fav_authors = [i for i in storage.all("FavoriteAuthor").values() if i.user_id == user_id]
    fav_genres = [i for i in storage.all("FavoriteGenre").values() if i.user_id == user_id]

    hot_books = {}
    fav_books = []

    if len(fav_authors) > 0:
        
        for i in fav_authors:
            book_authors = [j for j in storage.all("BookAuthor").values() if j.author_id == i["author_id"]]

            for book_author in book_authors:
                reviews = len([j for j in storage.all('Review').values() if j.book_id == book_author.book_id])
                book = storage.get("Book", book_author.book_id)
                book["reviews_count"] = reviews
                hot_books[book["id"]] = reviews
                fav_books.append(book)

    if len(fav_genres) > 0:
        hot_list2 = {}

        for i in fav_genres:
            book_genres = [j for j in storage.all("BookGenre").values() if j.genre_id == i["genre_id"]]

            for book_genre in book_genres:
                reviews = len([j for j in storage.all('Review').values() if j.book_id == book_genre.book_id])
                book = storage.get("Book", book_genre.book_id)
                book["reviews_count"] = reviews
                hot_list2[book["id"]] = reviews
                fav_books.append(book)
        hot_books = {**hot_books, **hot_list2}

    # sort the items based on the review count and pick the first ten
    hot_books = sorted(hot_books, key=lambda item: item[1], reverse=True)[:10] 
    for i in fav_books:
        if i["id"] not in hot_books:
            del i

    # get rid of duplicates
    fav_books = {tuple(sorted(i.items())) for i in fav_books}
    fav_books = [dict(item) for item in fav_books]

    return jsonify(fav_books)
