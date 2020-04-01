"""
Message Model
"""
from datetime import datetime
from typing import Dict, Any

import sqlalchemy as db  # type: ignore

from . import Base


class Message(Base):
    """
    Message Model

    Attributes
    ----------

    id: int [PK]
         unique identifier

    reciever_message: String(512)
         Encrypted message for the Reciever (encrypted with their public_key)

    sender_message: String(512)
         Encrypted message for the Sender (encrypted with their public_key)

    date: Time
         Date the message was sent to the server

    edited: Boolean
         Whether or not the message was editted

    read: Boolean
         Whether the message was read by the reciever or not

    sender: String(64) [FK]
         Sender of the message (their handle)

    reciever: String(64) [FK]
         Reciever of the message (their handle)
    """

    __tablename__ = "Message"

    id = db.Column(
        db.Integer,
        db.Sequence("message_id", start=0, increment=1),
        primary_key=True,
        nullable=False,
    )
    reciever_message = db.Column(db.String(512), nullable=False)
    sender_message = db.Column(db.String(512), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False)

    sender = db.Column(db.String(64), db.ForeignKey("User.handle"))
    reciever = db.Column(db.String(64), db.ForeignKey("User.handle"))

    def to_reciever_json(self) -> Dict[str, Any]:
        """
        Reciever JSON

        Returns
        -------

        Dict[str, Any]
        {
          "id": self.id,
          "sender": self.sender,
          "message": self.reciever_message,
          "date": self.date,
          "edited": self.edited
        }
        """
        return {
            "id": self.id,
            "sender": self.sender,
            "message": self.reciever_message,
            "date": self.date,
            "edited": self.edited,
        }

    def to_sender_json(self) -> Dict[str, Any]:
        """
        Sender JSON

        Returns
        -------

        Dict[str, Any]
        {
          "id": self.id,
          "message": self.reciever_message,
          "date": self.date,
          "edited": self.edited,
          "read": self.read
        }
        """
        return {
            "id": self.id,
            "message": self.sender_message,
            "date": self.date,
            "edited": self.edited,
            "read": self.read,
        }
