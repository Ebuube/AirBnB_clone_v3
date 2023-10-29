#!/usr/bin/python3
"""
Manage a User object
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from flask import make_response
from flask import abort
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieve the list of all User objects
    """
    users = list()
    objs = storage.all(User)
    for user in objs.values():
        users.append(user.to_dict())

    return make_response(jsonify(users))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieve a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return make_response(jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    # craft response
    response = make_response(jsonify(dict()))
    response.status_code = 200
    return response


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Create a User object
    """
    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    required_attrs = ['email', 'password']
    for attr in required_attrs:
        if attr not in request.get_json():
            msg = "Missing {}".format(attr)
            response = make_response(jsonify({'error': str(msg)}))
            response.status_code = 400
            abort(response)

    new = User()
    for attr in required_attrs:
        setattr(new, attr, request.get_json().get(attr))
    new.save()

    # Craft response
    response = make_response(jsonify(new.to_dict()))
    response.status_code = 201
    return response


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Update a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if type(request.get_json()) not in (str, dict):
        response = make_response(jsonify({'error': 'Not a JSON'}))
        response.status_code = 400
        abort(response)

    # update
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(user, key, val)
    user.save()

    # craft response
    response = make_response(jsonify(user.to_dict()))
    response.status_code = 200
    return response
