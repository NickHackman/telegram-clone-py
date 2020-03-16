#!/usr/bin/env python3
from pathlib import Path
import os
import re

from typing import Final, List, Any, Pattern

from .image_button import ImageButton

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QListView,
)

MENU_ICON: Final[
    str
] = f"{Path(__file__).parent.parent.absolute()}{os.sep}assets{os.sep}menu.svg"


class ChatList(QWidget):
    _list_view: QListView

    _chats: Final[List[Any]] = ["hi", "meow", "cat"]
    _displayed_chats: List[Any] = ["hi", "meow", "cat"]

    def __init__(self):
        """
        ChatList that has a header that filters chats
        """
        QWidget.__init__(self)
        header_layout: QHBoxLayout = self._construct_header()
        model = QStringListModel(self._displayed_chats)
        self._list_view = QListView()
        self._list_view.setModel(model)
        layout = QVBoxLayout(self)
        layout.addLayout(header_layout)
        layout.addWidget(self._list_view)

    def _construct_header(self) -> QHBoxLayout:
        """
        Constructs the Chat List Header

        Has a search bar and a menu button

        Returns
        -------

        QHBoxLayout
             The Layout for the Header
        """
        image_button: ImageButton = ImageButton(MENU_ICON, lambda: print(10))
        text_input: QLineEdit = QLineEdit()
        text_input.setPlaceholderText("Search")
        text_input.textChanged.connect(lambda s: self._search_chats(s))
        # TODO: Size search bar to be height of Menu icon
        header_layout = QHBoxLayout()
        header_layout.addWidget(image_button)
        header_layout.addWidget(text_input)
        return header_layout

    def _search_chats(self, regex: str) -> None:
        """
        Searches Chats based on Regular Expression

        Parameters
        ----------

        regex: str
             User provied regular expression to use on chats
        """
        try:
            REGEX: Final[Pattern] = re.compile(regex)
            self._displayed_chats = list(
                filter(lambda chat: REGEX.match(chat), self._chats)
            )
            # Update Model
            self._list_view.setModel(QStringListModel(self._displayed_chats))
        except (SyntaxError, re.error):
            pass
