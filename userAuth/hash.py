import hashlib
import os
import database.userAuth

def hash_password(password: str) -> tuple:
    salt = os.urandom(16)
    salted_password = salt + password.encode()
    hashed_password = hashlib.pbkdf2_hmac('sha256', salted_password, salt, 100000)
    return (salt,hashed_password)


def verify_password(email:str,provided_password: str) -> bool:
    stored_password = database.userAuth.full_user_info_by_email(email)["password_hash"]
    stored_salt = database.userAuth.full_user_info_by_email(email)["salt"]
    salted_password = stored_salt + provided_password.encode()
    hashed_password = hashlib.pbkdf2_hmac('sha256', salted_password, stored_salt, 100000)
    return hashed_password == stored_password

