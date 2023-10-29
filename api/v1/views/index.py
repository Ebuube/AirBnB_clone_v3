#!/usr/bin/python3
"""
Create index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.user import User

classes = [Amenity, Place, City, Review, State, User]


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Check if api is available or not
    """
    status = {"status": "OK"}

    return jsonify(status)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """
    Retrieve the number of each objects by type
    """
    stats = dict()
    for cls in classes:
        stats[cls.__tablename__] = storage.count(cls)

    return jsonify(stats)
