"""
Module that contains all SQLAlchemy Models used for Telegram-clone-py

Models
------

User

UserInfo

Message
"""
import os
from pathlib import Path
from typing import Any

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import scoped_session  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore


DB_URI: str = (
    f"sqlite:////{Path(__file__).parent.parent.absolute()}{os.sep}telegram-clone-py.db"
)
engine = db.create_engine(DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base: Any = declarative_base()
Base.metadata.bind = engine

# Import models to create tables
# Imported here because Base is passed into them
from .user import User
from .user_info import UserInfo
from .message import Message


Base.metadata.create_all()
