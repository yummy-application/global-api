from flask import Flask


from userAuth.accCreation import account_creation
from userAuth.verificationEmail import email_verification


app = Flask(__name__)
app.register_blueprint(account_creation)
app.register_blueprint(email_verification)
app.run(host="0.0.0.0", port=3184)