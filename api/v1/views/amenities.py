#!/usr/bin/python3
"""
Manage a Amenity object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieve the list of all Amenity objects
    """
    amenities = list()
    objs = storage.all(Amenity)
    for amenity in objs.values():
        amenities.append(amenity.to_dict())

    return make_response(jsonify(amenities))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieve a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return make_response(jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """
    Create a Amenity object
    """
    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)
    if 'name' not in request.get_json():
        response = make_response(jsonify({'error': 'Missing name'}))
        response.status_code = 400
        abort(response)

    new = Amenity(name=request.get_json().get('name'))
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
    amenity.save()

    # craft response
    response = make_response(jsonify(amenity.to_dict()))
    response.status_code = 200
    return response
