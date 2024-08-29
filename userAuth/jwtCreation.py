import os
import time
from logging import DEBUG

import jwt
from dotenv import load_dotenv


def create_token(user_id, username, email, user_role):
    load_dotenv()
    return jwt.encode(headers={"type": "JWT", "alg": "HS256"},
               payload={"iss": "yummy", "sub": user_id, "exp": int(time.time()) + 300,
                        "iat": int(time.time()), "user": username, "role": user_role, "email": email},
               algorithm="HS256", key=os.environ.get("JWT_SECRET"))

def jwt_is_valid(jwt_token):
    """
        Checks if a given JWT token is valid.
        Args:
            jwt_token (str): The JWT token to be validated.
        Returns:
            dict or bool: The decoded JWT token data if valid, False otherwise.
        """
    load_dotenv()
    try:
        data =jwt.decode(jwt_token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        return False
    return data