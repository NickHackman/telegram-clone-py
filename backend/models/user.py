from typing import Dict

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "user"
    """
    User Db Model

    Attributes
    ----------

    handle: str
    info: FK("UserInfo")

    """

    handle = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(255), db.ForeignKey("userinfo.email"))
    userinfo = relationship("UserInfo", back_populates="users")

    def __repr__(self) -> str:
        return f"<User @{self.handle}>"

    def to_json(self) -> Dict[str, str]:
        info_json = self.userinfo.to_json()
        info_json["handle"] = self.handle
        return info_json
