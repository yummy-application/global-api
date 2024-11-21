import json
import os
import secrets
import time
import flask
import jwt
from dotenv import load_dotenv
from flask import Blueprint, Response

import database.userAuth


def create_jwt_token(user_id, username, email, user_role):
    load_dotenv()
    return jwt.encode(headers={"type": "JWT", "alg": "HS256"},
                      payload={"iss": "yummy", "sub": user_id, "exp": int(time.time()) + 300,
                               "iat": int(time.time()), "user": username, "role": user_role, "email": email},
                      algorithm="HS256", key=os.environ.get("JWT_SECRET"))


def jwt_is_valid(jwt_token):
    load_dotenv()
    try:
        data = jwt.decode(jwt_token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        return False
    return data


jwt_recreation = Blueprint('jwtRecreation', __name__, template_folder='templates')


@jwt_recreation.route('/acc/jwt/refresh', methods=['POST'])
def refresh_jwt():
    request_data = flask.request.json
    refresh_token = request_data['refreshToken']
    email = request_data['email']
    if not database.userAuth.validate_refresh_token(refresh_token):
        return Response(response="Invalid refresh token", status=401)
    user_data = database.userAuth.full_user_info_by_email(email)
    new_jwt = create_jwt_token(user_data["user_id"], user_data["username"], email, user_data["role"])
    new_refresh_token = secrets.token_urlsafe(32)
    database.userAuth.create_user_refresh_token(user_data["user_id"], new_refresh_token)
    return flask.jsonify({"jwt": new_jwt, "refreshToken": new_refresh_token})
