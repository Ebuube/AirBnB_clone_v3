#!/usr/bin/python3
"""
Manage a Place object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieve the list of all Place objects
    """
    places = list()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if city.places is not None:
        for place in city.places:
            places.append(place.to_dict())

    return make_response(jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieve a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return make_response(jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create a Place object
    """
    city = storage.get(City, city_id)
    if city is None:
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

    required_attrs = ['user_id', 'city_id', 'name']
    for attr in required_attrs:
        if attr not in request.get_json():
            msg = "Missing {}".format(attr)
            response = make_response(jsonify({'error': str(msg)}))
            response.status_code = 400
            abort(response)

    new = Place()
    # defaults
    allowed_attrs = {
                "description": "",
                "number_rooms": 0,
                "number_bathrooms": 0,
                "max_guest": 0,
                "price_by_night": 0,
                "latitude": 0.0,
                "longitude": 0.0
    }
    for attr, val in allowed_attrs.items():
        setattr(new, attr, val)

    # Requested
    for attr in request.get_json():
        if attr in allowed_attrs or attr in required_attrs:
            setattr(new, attr, request.get_json().get(attr))
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Update a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(place, key, val)
    place.save()

    # craft response
    response = make_response(jsonify(place.to_dict()))
    response.status_code = 200
    return response
