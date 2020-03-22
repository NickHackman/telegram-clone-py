from typing import Dict

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from . import Base


class UserInfo(Base):
    __tablename__ = "UserInfo"
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

    handle = db.Column(db.String(64), db.ForeignKey("User.handle"))
    email = db.Column(db.String(255), primary_key=True)
    bio = db.Column(db.String(144))
    public_key = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<UserInfo {self.email}>"

    def to_json(self) -> Dict[str, str]:
        return {
            "bio": self.bio,
            "public_key": self.public_key.decode(),
            "verified": self.verified,
        }
