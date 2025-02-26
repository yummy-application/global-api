import secrets
import time

import flask
from flask import Blueprint, Response

import userAuth.jwtCreation as jwtAuth
import database
from database import userAuth
from userAuth.hash import verify_password

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/acc/login/credentials', methods=['POST'])
def login_with_credentials_and_get_new_tokens():
    email = flask.request.json.get('email').lower()
    password = flask.request.json.get('password')
    if not database.userAuth.user_exists(email):
        return Response(response="User doesn't exist", status=404)
    if not verify_password(email, password):
        return Response(response="Wrong password", status=401)
    user_data = database.userAuth.full_user_info_by_email(email)
    json_web_token = jwtAuth.create_jwt_token(user_data["user_id"], user_data["username"], email,
                                                           user_data["role"])
    refresh_token = secrets.token_urlsafe(32)  # todo send email
    database.userAuth.create_user_refresh_token(user_data["user_id"], refresh_token)
    if not database.userAuth.email_is_verified(email):
        return flask.jsonify({"jwt": json_web_token, "refreshToken": refresh_token, "userId": user_data["user_id"]}) ,202
    return flask.jsonify({"jwt": json_web_token, "refreshToken": refresh_token, "userId": user_data["user_id"]})



@login.route("/acc/login/check", methods=["POST"])
def validate_jwt():
    jwt = flask.request.headers.get('jwt')
    jwt_data = jwtAuth.jwt_is_valid(jwt)
    if not jwt_data:
        return Response(response="Invalid jwt", status=401)
    if time.time() > jwt_data["exp"]:
        return Response(response="Jwt expired", status=499)
    return Response(response="Valid jwt", status=200)