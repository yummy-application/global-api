import secrets

import flask
from flask import Blueprint, Response

import userAuth.jwtCreation
import database
from database import userAuth

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/acc/login/credentials', methods=['POST'])
async def login_with_credentials_and_get_new_tokens():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    if not database.userAuth.check_user_credentials(email, password):
        return Response(response="Invalid email or Password", status=401)
    if not database.userAuth.email_is_verified(email):
        return Response(response="Email is not verified", status=200)
    user_info = database.userAuth.full_user_info_by_email(email)
    jwt_token = userAuth.jwtCreation.create_token(user_info["user_id"], user_info["username"], email, user_info["role"])
    refresh_token = secrets.token_urlsafe(32)
    database.userAuth.create_user_refresh_token(user_info["user_id"], refresh_token)
    return flask.jsonify({"jwt": jwt_token, "refreshToken": refresh_token}, 200)


