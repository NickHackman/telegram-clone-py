from pathlib import Path
import os
from typing import Any, Final

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from .image_button import ImageButton

from ..models import Chat, Message

USER_ICON: Final[
    str
] = f"{Path(__file__).parent.parent.absolute()}{os.sep}assets{os.sep}user.svg"


class ChatCard(QWidget):
    chat: Any

    def __init__(self, chat: Chat):
        """
        Constructs a ChatCard QWidget

        Parameters
        ----------

        chat: Any
             Chat Object
        """
        QWidget.__init__(self)
        self.chat = chat
        user_button: ImageButton = ImageButton(USER_ICON, lambda: print(10))
        user_button.setFixedSize(64, 64)
        layout = QHBoxLayout(self)
        layout.addWidget(user_button)
        body: QVBoxLayout = self._body()
        layout.addLayout(body)

    def _body(self) -> QVBoxLayout:
        LAST_MESSAGE: Message = self.chat.messages[-1]
        name: QLabel = QLabel(self.chat.other.handle)
        date: QLabel = QLabel(LAST_MESSAGE.date)
        top = QHBoxLayout()
        top.addWidget(name)
        top.addWidget(date)
        body = QVBoxLayout()
        body.addLayout(top)
        msg: QLabel = QLabel(f"{LAST_MESSAGE.sender}: {LAST_MESSAGE.message}")
        body.addWidget(msg)
        return body
