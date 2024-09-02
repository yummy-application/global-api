from mysql.connector.cursor_cext import CMySQLCursorBuffered

from database.database import get_connection


def check_if_email_already_used(email) -> bool:
    with get_connection() as db:
        cursor: CMySQLCursorBuffered = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM users WHERE email = %(email)s", {"email": email})
        return cursor.fetchone() is not None


def create_user(email, password, username, object_pronoun, subject_pronoun, possessive_pronoun, salt) -> dict:
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute(
            "INSERT INTO users (email, password_hash,username,object_pronoun,subject_pronoun,`possessive_pronoun`,salt) VALUES (%(email)s, %(password)s, %(username)s, %(object_pronoun)s, %(subject_pronoun)s, %(possessive_pronoun)s, %(salt)s)",
            {"email": email, "password": password, "username": username, "object_pronoun": object_pronoun,
             "subject_pronoun": subject_pronoun, "possessive_pronoun": possessive_pronoun, "salt": salt})
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


def create_user_refresh_token(user_id, token):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("INSERT INTO refresh_tokens (user_id, token) VALUES (%(user_id)s, %(token)s)",
                       {"user_id": user_id, "token": token})
        db.commit()


def validate_refresh_token(token: str):
    """
    Validates a given refresh token against the database.

    Args:
        token (str): The refresh token to be validated.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM refresh_tokens WHERE token = %(token)s", {"token": token})
        return cursor.fetchall()["refresh_token"] == token
