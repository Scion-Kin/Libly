#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import grand_view
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(grand_view)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


@app.errorhandler(400)
def invalid_json(error):
    ''' 400 Error
    ---
    responses:
        400:
        description: Invalid json in request
    '''

    return make_response(jsonify({'error': 'Invalid JSON'}), 415)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
