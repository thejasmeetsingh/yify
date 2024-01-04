"""
Contain a centralize util functions
"""
from datetime import datetime
from datetime import timedelta

import bcrypt
import jwt

import settings
import strings
from auth.models import User


def get_hashed_password(password: str) -> str:
    """
    Generate hashed password from raw password string
    """

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password(raw_password: str, hashed_password: str) -> bool:
    """
    Validate raw/input password with hashed password
    """

    return bcrypt.checkpw(
        raw_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def has_digits(password: str) -> bool:
    """
    Function for checking if password contains a digit or not
    :param password: A string containing password
    :return: Boolean depicting password contains a digit or not
    """

    return any(char.isdigit() for char in password)


def has_special_character(password: str) -> bool:
    """
    Function for checking if password contains a special character or not
    :param password: A string containing password
    :return: Boolean depicting password contains a special character or not
    """

    special_chars = "[!@#$%^&*()]"
    return any(char in special_chars for char in password)


def validate_password(password: str, email: str, first_name: str, last_name: str) -> str | None:
    """
    Perform basic password validation checks

    :param password: Raw password
    :param email: user email
    :param first_name: user first name
    :param last_name: user last name
    :return: String contains error message or None
    """

    if " " in password:
        error_message = strings.PASSWORD_CONTAINS_SPACES

    elif len(password) < 8:
        error_message = strings.PASSWORD_LENGTH_ERROR

    elif email in password or first_name in password or last_name in password:
        error_message = strings.PASSWORD_CONTAINS_NAME_EMAIL

    elif password.lower() == password:
        error_message = strings.PASSWORD_CONTAINS_LOWER_CHARS

    elif password.upper() == password:
        error_message = strings.PASSWORD_CONTAINS_UPPER_CHARS

    elif not has_digits(password):
        error_message = strings.PASSWORD_DIGITS_ERROR

    elif not has_special_character(password):
        error_message = strings.PASSWORD_SPECIAL_CHAR_ERROR

    else:
        error_message = None

    return error_message


def get_auth_token(data: dict, exp: timedelta) -> str:
    """
    Generate auth tokens for a user
    :param data: JWT payload
    :param exp: Timedelta containing the token expiration
    :return: string containing the JWT token
    """

    _data = data.copy()
    _data.update({"exp": datetime.utcnow() + exp})
    encoded_jwt = jwt.encode(payload=_data, key=settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def generate_auth_tokens(db_user: User) -> dict[str, str]:
    """
    Generate authentication tokens for a given user.
    :param db_user: DB user object
    :return: Dict containing auth tokens
    """

    payload = {"user_id": str(db_user.id)}

    access_token = get_auth_token(
        data=payload,
        exp=timedelta(minutes=int(settings.ACCESS_TOKEN_EXP_MINUTES))
    )
    refresh_token = get_auth_token(
        data=payload,
        exp=timedelta(minutes=int(settings.REFRESH_TOKEN_EXP_MINUTES))
    )

    return {
        "access": access_token,
        "refresh": refresh_token
    }


def get_jwt_payload(token: str) -> dict | None:
    """
    Validate refresh token
    :param token: String containing token
    :return: Dict containing payload or None if token is expired
    """

    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms="HS256")
        return payload
    except (jwt.ExpiredSignatureError, jwt.DecodeError) as _:
        return None


async def html_to_string(filename: str, context: dict) -> str:
    """
    Given a filename, Read the file and convert it from HTML to string

    :param filename: A string containing filename
    :param context: Dict containing the dynamic data for template
    :return: HTML string
    """

    template = settings.JINJA_TEMPLATE_ENV.get_template(filename)
    rendered_html = template.render(**context)
    return rendered_html
