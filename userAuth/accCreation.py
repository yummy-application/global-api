import os
import re
import secrets
import time
import flask
from dotenv import load_dotenv
from flask import Blueprint, Response


import database.userAuth
import userAuth.jwtCreation
import userAuth.hash

account_creation = Blueprint('account_creation', __name__, template_folder='templates')


@account_creation.route('/acc/create', methods=['POST'])
def create_account():
    email = flask.request.headers.get('email')
    password = flask.request.headers.get('password')
    username = flask.request.headers.get('username')
    subject_pronoun = flask.request.headers.get('subjectPronoun')
    object_pronoun = flask.request.headers.get('objectPronoun')
    possessive_pronoun = flask.request.headers.get('possessivePronoun')
    salt,password_hash = userAuth.hash.hash_password(password)
    email_regex = "^((?!\.)[\w\-_.]*[^.])@([\w-]+\.)+[\w-]{2,4}$"
    if not re.match(email_regex, email):
        return Response(response="Invalid email", status=400)
    if database.userAuth.check_if_email_already_used(email):
        return Response(response="Email already used", status=409)
    user_data = database.userAuth.create_user(email, password_hash, username, subject_pronoun, object_pronoun, possessive_pronoun,salt)
    user_id = user_data["user_id"]
    user_role = user_data["role"]
    json_web_token = userAuth.jwtCreation.create_token(user_id, username, email, user_role)
    refresh_token = secrets.token_urlsafe(32)
    database.userAuth.create_user_refresh_token(user_id, refresh_token)
    return flask.jsonify({"jwt": json_web_token, "refreshToken": refresh_token,"userId":user_id})
