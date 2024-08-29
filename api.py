from webbrowser import register

from flask import Flask


from userAuth.accCreation import account_creation
from userAuth.verificationEmail import email_verification
from userAuth.login import login


app = Flask(__name__)
app.register_blueprint(account_creation)
app.register_blueprint(email_verification)
app.register_blueprint(login)
app.run(host="0.0.0.0", port=3184,ssl_context="adhoc")