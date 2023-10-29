#!/usr/bin/python3
"""
Manage a City object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieve the list of all City objects
    """
    cities = list()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if state.cities is not None:
        for city in state.cities:
            cities.append(city.to_dict())

    return make_response(jsonify(cities))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieve a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return make_response(jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create a City object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)
    if 'name' not in request.get_json():
        response = make_response(jsonify({'error': 'Missing name'}))
        response.status_code = 400
        abort(response)

    new = City(name=request.get_json().get('name'), state_id=state_id)
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Update a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(city, key, val)
    city.save()

    # craft response
    response = make_response(jsonify(city.to_dict()))
    response.status_code = 200
    return response
