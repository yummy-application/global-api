from webbrowser import register

from flask import Flask

from user.info import user_info
from userAuth.accCreation import account_creation
from userAuth.jwtCreation import jwt_recreation
from userAuth.verificationEmail import email_verification
from userAuth.login import login


app = Flask(__name__)
app.register_blueprint(account_creation)
app.register_blueprint(email_verification)
app.register_blueprint(login)
app.register_blueprint(user_info)
app.register_blueprint(jwt_recreation)
app.run(host="0.0.0.0", port=3184)