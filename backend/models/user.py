#!/usr/bin/env python3
from typing import Dict

import sqlalchemy as db  # type: ignore

from . import Base


class User(Base):
    __tablename__ = "Users"
    """
    User Db Model

    Attributes
    ----------

    handle: str
    info: FK("UserInfo")

    """

    handle = db.Column(db.String(64), primary_key=True)
    info = db.Column(db.String(255), db.ForeignKey("UserInfo.email"))

    def __repr__(self) -> str:
        return f"<User @{self.handle} {self.email}>"

    def to_json(self) -> Dict[str, str]:
        info_json = self.info.to_json()
        info_json["handle"] = self.handle
        return info_json
