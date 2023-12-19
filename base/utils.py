"""
Contain a centralize util functions
"""
from datetime import timedelta
from datetime import datetime

import jwt
import bcrypt

import config


def get_hashed_password(password: str) -> str:
    """
    Generate hashed password from raw password string
    """

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def validate_password(raw_password: str, hashed_password: str) -> bool:
    """
    Validate raw/input password with hashed password
    """

    return bcrypt.checkpw(
        raw_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_auth_token(data: dict, exp: timedelta) -> str:
    """
    Generate auth tokens for a user
    :param data: JWT payload
    :param exp: Timedelta containing the token expiration
    :return: string containing the JWT token
    """

    _data = data.copy()
    _data.update({"exp": datetime.utcnow() + exp})
    encoded_jwt = jwt.encode(payload=_data, key=config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
