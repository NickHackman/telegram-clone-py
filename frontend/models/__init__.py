from dataclasses import dataclass
from typing import List

from .user import User
from .message import Message


@dataclass
class Chat:
    other: User
    messages: List[Message]
