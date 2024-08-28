from database.database import get_connection


def check_if_email_already_used(email) -> bool:
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %(email)s", {"email": email})
        return cursor.fetchnone() is not None


def create_user(email, password, username,object_pronoun,subject_pronoun,possessive_pronoun) -> dict:
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute(
            "INSERT INTO users (email, password_hash,username,object_pronoun,subject_pronoun,possessive_pronoun) VALUES (%(email)s, %(password)s, %(username)s, %(object_pronoun)s, %(subject_pronoun)s, %(possessive_pronoun)s)",
            {"email": email, "password": password, "username": username, "object_pronoun": object_pronoun, "subject_pronoun": subject_pronoun, "possessive_pronoun": possessive_pronoun})
        db.commit()
        cursor.execute("SELECT * FROM users WHERE email = %(email)s", {"email": email})
        return cursor.fetchall()[0]


def user_exists(email) -> bool:
    """
    Checks if a user with the given email exists in the database
    :param email: the user's email
    :return: bool
    """
    return check_if_email_already_used(email)

def full_user_info_by_email(email):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %(email)s", {"email": email})
        return cursor.fetchall()[0]

def verify_user(email):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("UPDATE users SET email_verified = 1 WHERE email = %(email)s", {"email": email})
        db.commit()
def email_is_verified(email) -> bool:
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT email_verified FROM users WHERE email = %(email)s", {"email": email})
        return cursor.fetchall()[0]["email_verified"]
def create_user_refresh_token(user_id,token):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("INSERT INTO refresh_tokens (user_id, token) VALUES (%(user_id)s, %(token)s)", {"user_id": user_id,"token":token})

def check_user_credentials(email, password_hash):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %(email)s AND password_hash = %(password_hash)s", {"email": email, "password_hash": password_hash})
        return cursor.fetchnone() is not None