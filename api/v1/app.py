#!/usr/bin/python3
"""
Simple Application
"""
from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views      # Why the views?
from os import getenv
from flask import make_response
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Registering the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(error):
    """
    End this session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handle 'NOT FOUND' error = 404
    """
    response = make_response(jsonify({"error": "Not found"}))
    response.status_code = 404
    return response


'''
@app.errorhandler(400)
def creation_error(error):
    """
    Handle errors generated while trying to create objects => 400
    """
    print("Creation error activated")
    response = make_response(jsonify({"error": error}))
    response.status_code = 400
    return response
'''


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'

    # app.run(host=host, port=port, threaded=True, debug=True)
    app.run(host=host, port=port, threaded=True)
