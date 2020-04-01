"""
Contains all components for the Backend of Telegram-clone-py

This file contains all HTTP Restful Routes
"""

import os
from pathlib import Path
from typing import Dict, Any, List

import bcrypt  # type: ignore
import jwt

from .rest import Rest, Method  # type: ignore
from .models import Session, User, UserInfo, Message
from .response import response, Status  # type: ignore
from .util import create_jwt, send_verification_email  # type: ignore

CONFIG_PATH = f"{Path(__file__).parent.absolute()}{os.sep}config.json"


rest: Rest = Rest(CONFIG_PATH)
secret = rest.get_secret()


def validate_user(info: UserInfo, token: str) -> bool:
    """
    Checks if a User's Token is valid

    Parameters
    ----------

    info: UserInfo
         UserInfo to check (solely email and password)

    token: str
         Json Web Token to check

    Returns
    -------

    True: User is valid
    False: User is invalid or has expired JWT
    """
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
        return data["email"] == info.email and data["password"] == info.password
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False


@rest.route("/user", Method.POST)
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
    user_info = UserInfo(
        email=payload["email"],
        bio=None,
        public_key=bytes(payload["public_key"].encode()),
        password=bcrypt.hashpw(payload["password"].encode(), bcrypt.gensalt()),
    )
    user = User(handle=payload["handle"], info=user_info)
    send_verification_email(
        user.info.email,
        rest.get_url(),
        create_jwt(user.info.email, user.info.password, secret, 24 * 7).decode(),
    )
    Session.add(user_info)
    Session.add(user)
    Session.commit()
    # Handle error with invalid email
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
    if not validate_user(user.info, token):
        return response(Status.Error, "Failed to validate token")
    send_verification_email(
        user.info.email,
        rest.get_url(),
        create_jwt(user.info.email, user.info.password, secret, 24 * 7).decode(),
    )
    return response(Status.Success, "Verification email sent")


@rest.route("/login", Method.POST)
def login(payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Logins in a User

    Parameters
    ----------

    email: str
         Email for User

    payload: Dict[Any, Any]
         Payload as
         {
          "email": "email_here",
          "password": "password_here"
         }

    Returns
    -------

    No User Exists or
    Password is incorrect or
    JSON Web Token to authenticate user and port to connect via websockets
    """
    email: str = payload["email"]
    user_info = Session.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info:
        return response(Status.Error, f"No user with email: {email}")
    if not bcrypt.checkpw(payload["password"].encode(), user_info.password):
        return response(Status.Failure, f"Password is incorrect")

    response_payload: Dict[str, Any] = {
        "token": create_jwt(user_info.email, user_info.password, secret).decode(),
        "public_key": user_info.public_key.decode(),
    }
    return response(Status.Success, response_payload)


@rest.route("/user/<handle>", Method.DELETE)
def delete_user(handle: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Deletes a User

    Parameters
    ----------

    handle: str
         Email of User to delete

    payload: Dict[any, any]
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
    if not validate_user(user.info, payload["token"]):
        return response(Status.Error, "Failed to validate token")
    Session.delete(user)
    Session.commit()
    return response(Status.Success, f"Successfully deleted {handle}")


@rest.route("/user/<handle>", Method.PUT)
def update_user(handle: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
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
          "token": "token_here",
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
    if not validate_user(user.info, payload["token"]):
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
    user = Session.query(User).filter(User.handle == handle).first()
    if not validate_user(user.info, token):
        return response(Status.Error, "Failed to validate token")
    user.info.verified = True
    Session.commit()
    return response(Status.Success, "Successfully verified email")


@rest.route("/users", Method.GET)
def list_users() -> Dict[Any, Any]:
    """
    Lists all Users by Handle

    Returns
    -------

    List[Dict[str, str]] of User information
    """
    users: List[User] = Session.query(User).all()
    users_json: List[Dict[str, str]] = [user.to_json() for user in users]
    return response(Status.Success, users_json)


@rest.route("/messages/<handle>/<token>", Method.GET)
def get_all_messages(handle: str, token: str) -> Dict[Any, Any]:
    """
    Get all messages sent and recieved for a User organized by other person

    Parameters
    ----------

    handle: str
         User's handle

    token: str
         User's JWT to validate them

    Returns
    -------

    Dict[Any, Any]
         Payload of all their messages
         where the other user's handle is the key followed by a List of messages
    """
    payload: Dict[str, List[Dict[str, str]]] = {}

    user = Session.query(User).filter(User.handle == handle).first()
    if not validate_user(user.info, token):
        return response(Status.Error, "Failed to validate token")
    messages: List[Message] = Session.query(Message).filter(
        Message.sender == handle or Message.reciever == handle
    ).all()
    for msg in messages:
        if msg.sender == handle and not msg.reciever in payload:
            payload[msg.reciever] = []
        elif msg.reciever == handle and not msg.sender in payload:
            payload[msg.sender] = []
        if msg.sender == handle:
            payload[msg.reciever].append(msg.to_sender_json())
        else:
            payload[msg.sender].append(msg.to_reciever_json())
    return response(Status.Success, payload)


@rest.route("/is/telegram-clone-server", Method.GET)
def is_telegram_clone_server() -> Dict[Any, Any]:
    """
    Whether or not a Server is a Telegram-clone-py server

    A way to verify that a server is connectable

    Returns
    -------

    bool of True
    """
    return response(Status.Success, True)


@rest.route("/message/<token>", Method.POST)
def send_message(token: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Send a message

    Parameters
    ----------

    token: str
          Token to validate the user

    Payload
    -------

    {
      "sender_message": "",
      "reciever_message": "",
      "sender": "",
      "reciever": "",
    }

    Returns
    -------

    Success message that said the message sent
    """
    user = Session.query(User).filter(User.handle == payload["sender"]).first()
    if not validate_user(user.info, token):
        return response(Status.Error, "Failed to validate user")
    message: Message = Message(
        reciever_message=payload["reciever_message"],
        sender_message=payload["sender_message"],
        sender=payload["sender"],
        reciever=payload["reciever"],
    )
    Session.add(message)
    Session.commit()
    return response(Status.Success, "Message sent")


rest.run()
