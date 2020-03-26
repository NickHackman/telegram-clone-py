"""
UserInfo Model
"""
from typing import Dict

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from . import Base


class UserInfo(Base):
    __tablename__ = "UserInfo"
    """
    UserInfo Model

    Attributes
    ----------

    handle: String(64) [FK]
         Handle of the user this information belongs to

    email: String(255) [PK]
         Email of User

    bio: String(144)
         Biography for the User

    public_key: String
         RSA Public key used to encrypt messages sent to them

    password: String
         User's encrypted password

    verified: Boolean
         Whether the User has verified their email address
    """

    handle = db.Column(db.String(64), db.ForeignKey("User.handle"))
    email = db.Column(db.String(255), primary_key=True)
    bio = db.Column(db.String(144))
    public_key = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<UserInfo {self.email}>"

    def to_json(self) -> Dict[str, str]:
        """
        All public fields to JSON

        Returns
        -------

        Dict[str, str]
        {
        "bio": self.bio,
        "public_key": self.public_key.decode(),
        "verified": self.verified
        }
        """
        return {
            "bio": self.bio,
            "public_key": self.public_key.decode(),
            "verified": self.verified,
        }
