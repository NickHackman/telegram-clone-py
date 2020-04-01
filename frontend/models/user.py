from dataclasses import dataclass


@dataclass
class User:
    handle: str
    public_key: str
    bio: str
