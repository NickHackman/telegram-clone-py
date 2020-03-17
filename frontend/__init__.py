#!/usr/bin/env python3
import sys

# from .components.chat_list import ChatList
from PyQt5.QtWidgets import QApplication
from typing import List

from .screens.create_account import CreateAccount
from .models import Chat, User, Message

chats: List[Chat] = [
    Chat(User("", "idk_a_public_key", "A"), [Message("hi", "A", "You", "now")],),
    Chat(
        User("", "idk_a_public_key", "B"),
        [Message("I use Arch Btw", "You", "B", "now")],
    ),
]

app = QApplication(sys.argv)
window = CreateAccount()
window.show()
app.exec_()
