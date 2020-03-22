from datetime import datetime
from typing import Dict, Any

import sqlalchemy as db  # type: ignore

from . import Base


class Message(Base):
    __tablename__ = "Message"

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    reciever_message = db.Column(db.String(512), nullable=False)
    sender_message = db.Column(db.String(512), nullable=False)
    date = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False)

    sender = db.Column(db.String(64), db.ForeignKey("User.handle"))
    reciever = db.Column(db.String(64), db.ForeignKey("User.handle"))

    def to_reciever_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender": self.sender,
            "message": self.reciever_message,
            "date": self.date,
            "edited": self.edited,
        }

    def to_sender_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender_message": self.sender_message,
            "date": self.date,
            "edited": self.edited,
            "read": self.read,
        }
