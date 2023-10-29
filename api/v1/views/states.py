#!/usr/bin/python3
"""
Create index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import make_response


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
