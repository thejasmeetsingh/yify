"""
Contain all user and auth related routes
"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import exc
from sqlalchemy.orm import Session

import config
import strings
from auth import crud
from auth.models import User
from auth.schemas import (
    UserCreate,
    UserJWT,
    JWT,
    UserLogin,
    RefreshToken,
    RefreshTokenResponse,
    UserResponse, UserUpdate, UserMessageResponse, ChangePassword, ResetPassword
)
from base.dependencies import get_db, get_current_user
from base.emails import send_mail
from base.utils import (
    check_password,
    generate_auth_tokens,
    get_jwt_payload,
    validate_password,
    get_hashed_password, get_auth_token, html_to_string
)

router = APIRouter()
templates = Jinja2Templates(directory=config.TEMPLATES_PATH)


@router.post(path="/register/", response_model=UserJWT, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """
    Handler for creating a user object in DB when user signup/register themselves

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    try:
        # Check if user already exists
        db_user = crud.get_user_by_email(db=db, email=user.email)
        if db_user:
            raise HTTPException(
                detail=strings.EMAIL_ALREADY_EXISTS,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Validate password
        password_error = validate_password(
            password=user.password,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )

        if password_error:
            raise HTTPException(
                detail=password_error,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        db_user = crud.create_user(db=db, user=user)

        # Generate auth tokens
        auth_tokens = generate_auth_tokens(db_user)
        jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

        return UserJWT(message=strings.ACCOUNT_CREATED_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.post(path="/login/", response_model=UserJWT, status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Annotated[Session, Depends(get_db)]):
    """
    Login API handler

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    try:
        # Check if user exists by the given email
        db_user = crud.get_user_by_email(db=db, email=user.email)
        if not db_user:
            raise HTTPException(
                detail=strings.USER_DOES_NOT_EXISTS,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check user password
        if not check_password(raw_password=user.password, hashed_password=db_user.password):
            raise HTTPException(
                detail=strings.INVALID_PASSWORD,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Generate auth tokens
        auth_tokens = generate_auth_tokens(db_user)
        jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

        return UserJWT(message=strings.LOGIN_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.post(
    path="/refresh-token/",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK
)
async def refresh_token(token: RefreshToken, db: Annotated[Session, Depends(get_db)]):
    """
    API handler for refreshing access token

    :param token: Refresh token instance
    :param db: DB session object
    :return: Pydantic JWT model instance
    """

    # Perform validations checks on the token
    if not token.refresh_token:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    payload = get_jwt_payload(token.refresh_token)

    if not payload:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Generate auth tokens
    auth_tokens = generate_auth_tokens(db_user)
    jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

    return RefreshTokenResponse(message=strings.TOKEN_REFRESH_SUCCESS, data=jwt)


@router.get(path="/profile/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def profile_details(user: Annotated[User, Depends(get_current_user)]):
    """
    API for fetching current user profile details

    :param user: User object
    :return: Instance of user response schema
    """

    return UserResponse(message=strings.PROFILE_DETAILS_SUCCESS, data=user)


@router.patch(path="/profile/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_profile_details(
        user_update: UserUpdate,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Update user profile details

    :param user_update: Contains updated profile data
    :param user: Current user object
    :param db: DB session object
    :return: User response schema instance
    """

    try:
        updated_data = user_update.model_dump(exclude_unset=True)
        # Check if the passed data is empty
        if not updated_data:
            raise HTTPException(
                detail=strings.INVALID_DATA_PASSED,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Update user details
        updated_user = crud.update_user(db=db, user=user, updated_data=updated_data)
        return UserResponse(message=strings.PROFILE_DETAILS_UPDATED, data=updated_user)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.delete(path="/profile/", response_model=UserMessageResponse, status_code=status.HTTP_200_OK)
async def delete_profile(
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Delete user profile details

    :param user: Current user object
    :param db: DB session object
    :return: Instance of User delete response schema
    """

    try:
        crud.delete_user(db=db, user=user)
        return UserMessageResponse(message=strings.PROFILE_DELETE_SUCCESS)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.put(
    path="/change-password/",
    response_model=UserMessageResponse,
    status_code=status.HTTP_200_OK
)
async def update_password(
        change_password: ChangePassword,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Change/Update current user password

    :param change_password: Instance of change password schema
    :param user: Current user object
    :param db: DB session object
    :return: Instance of User message schema
    """
    try:
        # Check if old and new password is empty or not
        if not change_password.old_password or not change_password.new_password:
            raise HTTPException(
                detail=strings.PASSWORD_EMPTY_ERROR.format(
                    "old password" if not change_password.old_password else "new password"
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Validate old password is correct or not
        if not check_password(
                raw_password=change_password.old_password,
                hashed_password=user.password
        ):
            raise HTTPException(
                detail=strings.OLD_PASSWORD_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if both old and new password are same
        if change_password.old_password == change_password.new_password:
            raise HTTPException(
                detail=strings.PASSWORD_SAME_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Perform password validation checks on the new password
        password_error = validate_password(
            password=change_password.new_password,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )

        if password_error:
            raise HTTPException(
                detail=password_error,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Generate hashed password based on new password and update it
        hashed_password = get_hashed_password(change_password.new_password)
        crud.update_user(db=db, user=user, updated_data={"password": hashed_password})

        return UserMessageResponse(message=strings.PASSWORD_UPDATE_SUCCESS)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.post(
    path="/reset-password/",
    response_model=UserMessageResponse,
    status_code=status.HTTP_200_OK
)
async def get_reset_password_link(
        reset_password: ResetPassword,
        request: Request,
        db: Annotated[Session, Depends(get_db)]
):
    """
    Reset password route for getting reset password link

    :param reset_password: Instance of reset password schema
    :param request: request object
    :param db: DB session object
    :return: Instance of user message schema
    """

    if not reset_password.email:
        raise HTTPException(
            detail=strings.INVALID_EMAIL,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Check if user exists or not
    db_user = crud.get_user_by_email(db=db, email=reset_password.email)

    if not db_user:
        raise HTTPException(
            detail=strings.USER_DOES_NOT_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Generate a token for reset password link
    token = get_auth_token(
        data={"user_id": str(db_user.id)},
        exp=timedelta(minutes=int(config.RESET_PASSWORD_EXP_MINUTES))
    )

    # Create the reset password link
    link = f"{request.url.scheme}://{request.url.hostname}"
    if request.url.port:
        link += f":{request.url.port}"

    link += f"/v1/reset-password-form/?token={token}"

    html = await html_to_string(filename="reset_password.html", context={"link": link})
    is_send_successfully = await send_mail(title="Reset Password", html=html)

    if not is_send_successfully:
        raise HTTPException(
            detail=strings.EMAIL_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return UserMessageResponse(message=strings.RESET_PASSWORD_LINK_SUCCESS)


@router.get(
    path="/reset-password-form/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_reset_password_form(request: Request, token: str):
    """
    Render reset password form.

    :param request: Request object
    :param token: String containing JWT token for reset password
    :return: Jinja template response
    """

    return templates.TemplateResponse(
        name="reset_password_form.html",
        context={
            "request": request,
            "is_valid": False,
            "token": token
        }
    )


@router.post(
    path="/validate-password/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def process_reset_password_form(
        request: Request,
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()],
        token: Annotated[str, Form()],
        db: Annotated[Session, Depends(get_db)]
):
    """
    Process reset password form data

    :param request: Request object
    :param password: New password
    :param confirm_password: New confirm password
    :param token: String containing reset password token
    :param db: DB session object
    :return: Jinja template response
    """

    context = {
        "request": request,
        "message": strings.PASSWORD_UPDATE_SUCCESS,
        "token": token
    }
    is_password_valid = True
    payload = get_jwt_payload(token)

    if not payload:
        context["message"] = strings.INVALID_RESET_PASSWORD_LINK
        is_password_valid = False

    user_id = payload.get("user_id")

    if not user_id and is_password_valid:
        context["message"] = strings.INVALID_RESET_PASSWORD_LINK
        is_password_valid = False

    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user and is_password_valid:
        context["message"] = strings.INVALID_RESET_PASSWORD_LINK
        is_password_valid = False

    if password != confirm_password and is_password_valid:
        context["message"] = strings.PASSWORD_NOT_MATCH
        is_password_valid = False

    if is_password_valid:
        password_error = validate_password(
            password=password,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )

        if password_error:
            context["message"] = password_error
            is_password_valid = False

    if is_password_valid:
        # Generate hashed password based on new password and update it
        hashed_password = get_hashed_password(confirm_password)
        crud.update_user(db=db, user=db_user, updated_data={"password": hashed_password})
        context["is_valid"] = is_password_valid

    return templates.TemplateResponse(name="reset_password_form.html", context=context)
