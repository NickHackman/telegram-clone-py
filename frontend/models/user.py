#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class User:
    bio: str
    public_key: str
    handle: str
