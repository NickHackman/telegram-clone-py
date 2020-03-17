from typing import Dict

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import relationship

from . import Base


class UserInfo(Base):
    __tablename__ = "userinfo"
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
    bio = db.Column(db.String(144))
    public_key = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)

    users = relationship("User", back_populates="userinfo")

    def __repr__(self) -> str:
        return f"<UserInfo {self.email}>"

    def to_json(self) -> Dict[str, str]:
        return {
            "bio": self.bio,
            "public_key": self.public_key.decode(),
            "verified": self.verified,
        }
