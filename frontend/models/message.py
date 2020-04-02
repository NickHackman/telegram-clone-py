from dataclasses import dataclass


@dataclass
class Message:
    id: int
    message: str
    reciever: str
    sender: str
    date: str
