#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Message:
    message: str
    reciever: str
    sender: str
    date: str
