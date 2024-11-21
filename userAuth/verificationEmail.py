import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import flask
from appwrite.services.users import Users
from dotenv import load_dotenv
from flask import Blueprint

import database.userAuth
import config.Appwrite

email_verification = Blueprint('email_verification', __name__, template_folder='templates')


@email_verification.route('/acc/verify', methods=['GET'])
def verify_email():
    mail = flask.request.args.get('mail')
    if not database.userAuth.user_exists(mail):
        return "User with this mail does not exist"
    if database.userAuth.full_user_info_by_email(mail)['email_verified']:
        return "User is already verified"
    database.userAuth.verify_user(mail)
    users = Users(config.Appwrite.APW_client)
    user_data = database.userAuth.full_user_info_by_email(mail)
    result = users.create_md5_user(
        user_id=user_data["username"],
        email=mail,
        password=user_data["password_hash"],
    )
    return "<html><body><h4>User verified (You can now close this site)</h4></body></html>"


def send_verification_email(receiver):
    load_dotenv()
    sender = "yummy verification <from@example.com>"
    receiver = f"<{receiver}>"
    verification_link = f"http://localhost:5000/acc/verify?mail={receiver}"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verify Your Email Address"
    msg['From'] = sender
    msg['To'] = receiver
    text = f"""\
    Hi,
    Thank you for signing up with us! To complete your registration, please use the following link to verify your email address:
    {verification_link}

    If you did not sign up for an account, please ignore this email. No action is required on your part.

    If you believe this email was sent to you in error or if you need help with your account, please contact our support team at support@example.com.

    Thank you!
    Best regards,
    Your yummy Team
    """

    html = f"""\
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        color: #333;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
      }}
      .container {{
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        box-sizing: border-box;
      }}
      h1 {{
        color: #007bff;
      }}
      p {{
        line-height: 1.6;
      }}
      a {{
        text-decoration: none;
        color: #ffffff;
      }}
      .button {{
        display: inline-block;
        padding: 12px 24px;
        font-size: 16px;
        color: #ffffff;
        background-color: #007bff;
        border-radius: 5px;
        text-align: center;
        transition: background-color 0.3s ease;
      }}
      .button:hover {{
        background-color: #0056b3;
      }}
      .footer {{
        font-size: 14px;
        color: #666;
        text-align: center;
        margin-top: 20px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Welcome!</h1>
      <p>Thank you for signing up with us! To complete your registration, please click the button below to verify your email address:</p>
      <a href="{verification_link}" class="button">Verify Email</a>
      <p>If you did not sign up for an account, please ignore this email. No action is required on your part.</p>
      <p>If you believe this email was sent to you in error or if you need help with your account, please contact our support team at <a href="mailto:support@example.com">support@example.com</a>.</p>
      <p class="footer">Thank you!<br>Best regards,<br>Your yummy Team</p>
    </div>
  </body>
</html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(os.environ.get("MAILTRAP_USERNAME"), os.environ.get("MAILTRAP_PW"))
        server.sendmail(sender, receiver, msg.as_string())
