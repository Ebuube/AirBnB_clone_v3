#!/usr/bin/python3
"""
Simple Application
"""
from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views      # Why the views?
from os import getenv


app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(error):
    """
    End this session
    """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'

    # app.run(host=host, port=port, threaded=True, debug=True)
    app.run(host=host, port=port, threaded=True)
