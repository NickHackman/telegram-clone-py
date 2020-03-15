#!/usr/bin/env python3
import os
from pathlib import Path

import sqlalchemy as db
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# from .message import Message

DB_URI = (
    f"sqlite:////{Path(__file__).parent.parent.absolute()}{os.sep}telegram-clone-py.db"
)
engine = db.create_engine(DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.metadata.bind = engine

from .user import User

# from .message import Message


Base.metadata.create_all()
