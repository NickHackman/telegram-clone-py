"""
User Model
"""
from typing import Dict

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from . import Base


class User(Base):
    __tablename__ = "User"
    """
    User Model

    Attributes
    ----------

    handle: String(64) [PK]
         Handle of the user, essentially a username

    info: UserInfo
         info for a given user

    sent_msg: List[Message]
         Messages sent by the user

    recv_msg: List[Message]
         Messages recieved by the user
    """

    handle = db.Column(db.String(64), primary_key=True)
    info = relationship("UserInfo", foreign_keys="UserInfo.handle", uselist=False)
    sent_msg = relationship("Message", foreign_keys="Message.sender")
    recv_msg = relationship("Message", foreign_keys="Message.reciever")

    def __repr__(self) -> str:
        return f"<User @{self.handle}>"

    def to_json(self) -> Dict[str, str]:
        """
        Converts the User information to JSON

        Returns
        -------

        {
          "handle": self.handle,
          info...
        }
        """
        info_json = self.info.to_json()
        info_json["handle"] = self.handle
        return info_json
