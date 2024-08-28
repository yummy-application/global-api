import os
import re
import secrets
import time
import flask
from dotenv import load_dotenv
from flask import Blueprint, Response


import database.userAuth
import userAuth.jwtCreation

account_creation = Blueprint('account_creation', __name__, template_folder='templates')


@account_creation.route('/acc/create', methods=['POST'])
async def create_account():
    email = flask.request.form.get('email')
    password = flask.request.form.get('passwordHash')
    username = flask.request.form.get('username')
    subject_pronoun = flask.request.form.get('subjectPronoun')
    object_pronoun = flask.request.form.get('objectPronoun')
    possessive_pronoun = flask.request.form.get('possessivePronoun')
    email_regex = "/^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/gm"
    if not re.match(email_regex, email):
        return Response(response="Invalid email", status=400)
    if database.userAuth.check_if_email_already_used(email):
        return Response(response="Email already used", status=409)
    user_data = database.userAuth.create_user(email, password, username)
    user_id = user_data["user_id"]
    user_role = user_data["role"]
    json_web_token = userAuth.jwtCreation.create_token(user_id, username, email, user_role)
    refresh_token = secrets.token_urlsafe(32)
    database.userAuth.create_user_refresh_token(user_id, refresh_token)
    return flask.jsonify({"jwt": json_web_token, "refreshToken": refresh_token}, 200)
