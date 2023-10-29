#!/usr/bin/python3
"""
Create index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import make_response
from flask import abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieve the list of all State objects
    """
    states = list()
    objs = storage.all(State)
    for state in objs.values():
        states.append(state.to_dict())

    return make_response(jsonify(states))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieve a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return make_response(jsonify(state.to_dict()))
