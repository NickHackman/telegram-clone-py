#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Dict, Any, List

import bcrypt  # type: ignore
import jwt

from rest import Rest, Method  # type: ignore
from models import Session, User, UserInfo  # type: ignore
from response import response, Status  # type: ignore
from util import create_jwt, send_verification_email  # type: ignore

CONFIG_PATH = f"{Path(__file__).parent.absolute()}{os.sep}config.json"

rest: Rest = Rest(CONFIG_PATH)

secret = rest.get_secret()


@rest.route("/create/user", Method.POST)
def create_user(payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Creates a User from POST payload

    Parameters
    ----------

    payload: Dict[Any, Any]
         Payload of the form
         {
          "email": "email_here"*,
          "password": "password_here",
          "handle": "handle_here"*,
          "public_key": "public_key_here"
         }
         * required

    Returns
    -------

    User (without encrypted password)
    """
    user = User(handle=payload["handle"], email=payload["email"])
    user_info = UserInfo(
        email=payload["email"],
        public_key=bytes(payload["public_key"].encode()),
        password=bcrypt.hashpw(payload["password"].encode(), bcrypt.gensalt()),
        handle=payload["handle"],
    )
    send_verification_email(
        user.email,
        rest.get_url(),
        create_jwt(user.info.email, user.info.password, secret, 24 * 7).decode(),
    )
    Session.add(user_info)
    Session.add(user)
    # Handle error with invalid email
    Session.commit()
    return response(Status.Success, user.to_json())


@rest.route("/resend/<handle>/verification/<token>", Method.POST)
def resend_email_verificaiton(
    handle: str, token: str, payload: Dict[Any, Any]
) -> Dict[Any, Any]:
    """
    Resends the Verification email

    Parameters
    ----------

    email: str
         User's email

    token: str
         JWT Token to verify the user

    payload: Dict[Any, Any]
         Empty payload

    Returns
    -------

    Dict[Any, Any]
         No User with handle: {handle}
         Invalid token
         Verification email sent
         Invalid Token
    """
    user = Session.query(User).filter(User.handle == handle).first()
    if not user:
        return response(Status.Error, f"No User with handle: {handle}")
    try:
        json = jwt.decode(token, secret, algorithms=["HS256"])
        if json["email"] != user.info.email and json["password"] == user.info.password:
            return response(Status.Error, "Invalid token")
        send_verification_email(
            user.info.email,
            rest.get_url(),
            create_jwt(user.info.email, user.info.password, secret, 24 * 7).decode(),
        )
        return response(Status.Success, "Verification email sent")
    except jwt.DecodeError:
        return response(Status.Error, "Invalid Token")


@rest.route("/login/<email>", Method.POST)
def login(email: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Logins in a User

    Parameters
    ----------

    email: str
         Email for User

    payload: Dict[Any, Any]
         Payload sent as {"password": "password_here"}

    Returns
    -------

    No User Exists or
    Password is incorrect or
    JSON Web Token to authenticate user
    """
    user_info = Session.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info:
        return response(Status.Error, f"No user with email: {email}")
    if not bcrypt.checkpw(payload["password"].encode(), user_info.password):
        return response(Status.Failure, f"Password is incorrect")
    return response(
        Status.Success, create_jwt(user_info.email, user_info.password, secret).decode()
    )


@rest.route("/user/delete/<handle>/<token>", Method.DELETE)
def delete_user(handle: str, token: str) -> Dict[Any, Any]:
    """
    Deletes a User

    Parameters
    ----------

    handle: str
         Email of User to delete

    token: str
         JWT to authenticate User

    Returns
    -------

    No User with handle: {handle}
    Invalid token
    Successfully deleted {email}
    Failed to validate Token
    """
    user = Session.query(User).filter(User.handle == handle).first()
    if not user:
        return response(Status.Failure, f"No User with handle: {handle}")
    try:
        json = jwt.decode(token, secret, algorithms=["HS256"])
        if json["email"] != user.info.email and json["password"] == user.info.password:
            return response(Status.Error, "Invalid token")
        Session.delete(user)
        Session.commit()
        return response(Status.Success, f"Successfully deleted {handle}")
    except jwt.DecodeError:
        return response(Status.Error, "Failed to validate token")


@rest.route("/update/user/<handle>/<token>", Method.PUT)
def update_user(handle: str, token: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Updates a User

    Parameters
    ----------

    email: str
         Email to query for

    jwt: str
         JSON Web Token to validate User to permit updating

    payload: Dict[Any, Any]
         Payload of the form
         {
          "handle": "handle_here",
          "info": {
            "password": "password_here",
            "handle": "handle_here",
            "public_key": "public_key_here"
            "bio": "bio_here"
          }
         }

    Returns
    -------

    No User with handle: {handle}
    Updated User information
    """
    user = Session.query(User).filter(User.handle == handle)
    if not user:
        return response(Status.Failure, f"No User with handle: {handle}")
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.DecodeError:
        return response(Status.Error, "Failed to validate token")
    user.update(payload)
    Session.commit()
    return response(Status.Success, user.to_json())


@rest.route("/user/<handle>", Method.GET)
def get_user(handle: str) -> Dict[Any, Any]:
    """
    Gets a User by Email

    Parameters
    ----------

    email: str
         Email to query for

    Returns
    -------

    User information including public_key, bio, and handle
    """
    user = Session.query(User).filter(User.handle == handle).first()
    if not user:
        return response(Status.Failure, f"No Users with handle: {handle}")
    return response(Status.Success, user.to_json())


@rest.route("/verify/<handle>/<token>", Method.POST)
def verify_email(handle: str, token: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Verifiy Email address

    Parameters
    ----------

    handle: str
         User Handle

    token: str
         JWT for User

    payload: Dict[Any, Any]
         In this case this payload is empty
    """
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.DecodeError:
        return response(Status.Error, "Failed to validate token")
    user = Session.query(User).filter(User.handle == handle).first()
    user.info.verified = True
    Session.commit()
    return response(Status.Success, "Successfully verified email")


@rest.route("/list/users", Method.GET)
def list_users() -> Dict[Any, Any]:
    """
    Lists all Users by Handle

    Returns
    -------

    List[str] of User handles
    """
    users: List[User] = Session.query(User).all()
    users_json: List[Dict[str, str]] = [user.handle for user in users]
    return response(Status.Success, users_json)


rest.run()
