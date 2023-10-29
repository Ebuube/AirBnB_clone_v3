#!/usr/bin/python3
"""
Create index page
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def api_status():
    """
    Check if api is available or not
    """
    status = {"status": "OK"}

    return jsonify(status)
