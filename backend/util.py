import datetime
import smtplib

import jwt


def create_jwt(email: str, password: bytes, secret: str, duration: int = 24) -> bytes:
    """
    Constructs a JSON Web Token

    Parameters
    ----------

    email: str
         User Email address

    password: bytes
         User encrypted password

    secret: str
         Server secret passcode

    duration: int
         Hours to allow defaults to 24

    Returns
    -------

    A JWT with all this information encrypted
    """
    return jwt.encode(
        {
            "email": email,
            "password": password.decode(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=duration),
        },
        secret,
        algorithm="HS256",
    )


def send_verification_email(email: str, server_url: str, token: str) -> None:
    """
    Sends Verification Email

    Parameters
    ----------

    email: str
         Email address to send to

    token: str
         JWT with 7 days expiration date
    """

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("fb7544c35ebfc9", "5b92c9be84f60d")
        server.sendmail(
            "telegram-clone-py-automated-email-services",
            email,
            f"Verify your email by visiting {server_url}/verify/{email}/{token}",
        )
