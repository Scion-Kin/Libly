#!/usr/bin/python3
''' The reviews api handler '''
from api.v1.views import grand_view
from models import storage
from models.book import Book
from models.review import Review
from flask import jsonify


@grand_view.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    ''' get all reviews from the database '''

    reviews = [i.to_dict() for i in storage.all(Review).values()]
    return jsonify(reviews)


@grand_view.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    ''' get a certain review from the database '''

    review = [i.to_dict() for i in storage.all(Review).values() if i.id == review_id]
    return jsonify(review[0])
