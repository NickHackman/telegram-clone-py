#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Any

import sqlalchemy as db  # type: ignore
from sqlalchemy.orm import scoped_session  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore


DB_URI = (
    f"sqlite:////{Path(__file__).parent.parent.absolute()}{os.sep}telegram-clone-py.db"
)
engine = db.create_engine(DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base: Any = declarative_base()
Base.metadata.bind = engine

from .user import User


Base.metadata.create_all()
