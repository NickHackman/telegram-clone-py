from datetime import datetime

import sqlalchemy as db  # type: ignore

from . import Base


class Message(Base):
    __tablename__ = "Messages"

    recv_message = db.Column(db.String(512), nullable=False)
    send_message = db.Column(db.String(512), nullable=False)
    date = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    # edited = db.Column(db.Bool, default=False, nullable=False)

    user_email = db.Column(db.String(255), db.ForeignKey("User.email"))
