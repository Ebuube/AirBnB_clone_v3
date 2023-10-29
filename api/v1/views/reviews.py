#!/usr/bin/python3
"""
Manage a Review object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieve the list of all Review objects
    """
    reviews = list()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place.reviews is not None:
        for review in place.reviews:
            reviews.append(review.to_dict())

    return make_response(jsonify(reviews))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieve a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return make_response(jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create a Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # Needs to be executed first
    if 'user_id' not in request.get_json():
        msg = "Missing user_id"
        response = make_response(jsonify({'error': str(msg)}))
        response.status_code = 400
        abort(response)
    else:
        user = storage.get(User, request.get_json().get('user_id'))
        if user is None:
            abort(404)

    required_attrs = ['text']
    for attr in required_attrs:
        if attr not in request.get_json():
            msg = "Missing {}".format(attr)
            response = make_response(jsonify({'error': str(msg)}))
            response.status_code = 400
            abort(response)

    new = Review(place_id=place_id)
    attrs = ['user_id', 'text']
    for attr in attrs:
        setattr(new, attr, request.get_json().get(attr))
    print("new:\n{}".format(new))   # test
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Update a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(review, key, val)
    review.save()

    # craft response
    response = make_response(jsonify(review.to_dict()))
    response.status_code = 200
    return response
