#!/usr/bin/python3
"""
Manage the relationship between Place and Amenity object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from models import storage_t as storage_type
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Retrieve the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = list()
    if place.amenities is not None:
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())

    return make_response(jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def get_amenity_by_place_and_id(place_id, amenity_id):
    """
    Retrieve a State object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_t != 'db':
        place.amentiy_ids.remove(amenity.id)
    else:
        pass
        # place.amenities(
        # Complete this task

    return make_response(jsonify(dict()))


'''
@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """
    Create a State object
    """
    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)
    if 'name' not in request.get_json():
        response = make_response(jsonify({'error': 'Missing name'}))
        response.status_code = 400
        abort(response)

    new = State(name=request.get_json().get('name'))
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Update a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(state, key, val)
    state.save()

    # craft response
    response = make_response(jsonify(state.to_dict()))
    response.status_code = 200
    return response
'''
