import flask
from flask import Blueprint

import database.restaurants

restaurant_creation_blp = Blueprint('restaurant_creation', __name__, template_folder='templates')


@restaurant_creation_blp.route('/restaurant/create', methods=['POST'])
def create_restaurant():
    name = flask.request.headers.get('name')
    backend_address = flask.request.headers.get('backendAddress')
    image = flask.request.headers.get('image')
    password = flask.request.headers.get('password')
    location = flask.request.headers.get('location')
    database.restaurants.create_restaurant(name, backend_address, password, image)
    return flask.jsonify({"success": True})
