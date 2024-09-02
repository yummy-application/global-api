import time

import flask
from flask import Blueprint, Response

import database.userAuth
from userAuth import jwtCreation

user_info = Blueprint('user_info', __name__, template_folder='templates')


@user_info.route('/acc/info', methods=['POST'])
async def login_with_credentials_and_get_new_tokens():
    jwt = flask.request.headers.get('jwt')
    jwt_data = jwtCreation.jwt_is_valid(jwt)
    if not jwt_data:
        return Response(response="Invalid jwt", status=401)
    if time.time() > jwt_data["exp"]:
        return Response(response="Jwt expired", status=499)
    user_data = database.userAuth.full_user_info_by_email(jwt_data["email"])
    user_data["password_hash"] = "Not send via this endpoint"
    user_data["salt"] = "Not send via this endpoint"
    if not database.userAuth.email_is_verified(jwt_data["email"]):
        return flask.jsonify(user_data), 202
    return flask.jsonify(user_data)
