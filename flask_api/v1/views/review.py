#!/usr/bin/python3
''' The reviews api handler '''
from flask_api.v1.views import grand_view
from models import storage
from models.review import Review
from flask import jsonify, abort, request, make_response


@grand_view.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    ''' get all reviews from the database '''

    all = [i.to_dict() for i in storage.all(Review).values()]
    if len(all) == 0:
        abort(404)

    reviews = {}
    for i in all:
        reviews[i["text"]] = {}
        reviews[i["text"]]["data"] = i
    return jsonify(reviews)


@grand_view.route('/<string:book_id>/reviews', methods=['GET'], strict_slashes=False)
def get_book_reviews(book_id):
    ''' get all reviews on a certain book from the database '''

    reviews = [i.to_dict() for i in storage.all(Review).values() if i.book_id == book_id]
    return jsonify(reviews) if len(reviews) > 0 else abort(404)


@grand_view.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    ''' get a certain review from the database '''

    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    reviews = {}
    reviews[review.text] = {}
    reviews[review.text]["data"] = review.to_dict()
    return jsonify(reviews)


@grand_view.route('/reviews', methods=['POST'], strict_slashes=False)
def create_review():
    ''' creates a new review in the database '''

    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user id"}), 400)

    if "book_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing book id"}), 400)

#    if "password" not in request.get_json():
#        return make_response(jsonify({"error": "unauthorized"}), 401)

#    users = [i for i in storage.all("User").values() if i.password == request.get_json()["password"]]

#    if len(users) == 0:
#        return make_response(jsonify({"error": "unauthorized"}), 401)

    new_review = Review(**request.get_json())
    new_review.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@grand_view.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    ''' creates a new review in the database '''

    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "unauthorized"}), 401)

    admins = [i for i in storage.all("User").values() if i.password == request.get_json()["password"]]

    if len(admins) == 0:
        return make_response(jsonify({"error": "unauthorized"}), 401)

    review = storage.get(Review, review_id)
    if review is not None:
        review.text = request.get_json()["text"]
        review.save()
        return jsonify(review.to_dict())

    abort(404)


@grand_view.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    ''' creates a new review in the database '''

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "unauthorized"}), 401)

    admins = [i for i in storage.all("User").values() if i.password == request.get_json()["password"]]

    if len(admins) == 0:
        return make_response(jsonify({"error": "unauthorized"}), 401)

    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({})

    abort(404)
