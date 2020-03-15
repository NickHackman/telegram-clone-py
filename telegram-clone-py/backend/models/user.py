#!/usr/bin/env python3
from typing import Dict

import sqlalchemy as db

from . import Base


class User(Base):
    __tablename__ = "users"
    """
    User Db Model

    Attributes
    ----------

    Email: str [Primary Key]
    handle: str
    bio: str
    public_key: bytes
    password: str
    """

    email = db.Column(db.String(255), primary_key=True)
    handle = db.Column(db.String(64))
    bio = db.Column(db.String(144))
    public_key = db.Column(db.LargeBinary(4096), nullable=False)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User @{self.handle} {self.email}>"

    def to_json(self) -> Dict[str, str]:
        return {
            "email": self.email,
            "handle": self.handle,
            "bio": self.bio,
            "public_key": self.public_key.decode(),
            "verified": self.verified,
        }
