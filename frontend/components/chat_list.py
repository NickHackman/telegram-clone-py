#!/usr/bin/env python3
from pathlib import Path
import os
import re

from typing import Final, List, Any, Pattern

from ..models import Chat, Message, User

from .image_button import ImageButton
from .chat_card import ChatCard


from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QListWidgetItem,
    QListWidget,
)

MENU_ICON: Final[
    str
] = f"{Path(__file__).parent.parent.absolute()}{os.sep}assets{os.sep}menu.svg"


class ChatList(QWidget):
    _list_widget: QListWidget

    _chats: List[Chat]

    def __init__(self, chats: List[Chat]):
        """
        ChatList that has a header that filters chats

        Parameters
        ----------

        List[Chat]
             List of Chats
        """
        QWidget.__init__(self)
        self._chats = chats
        header_layout: QHBoxLayout = self._construct_header()
        self._construct_list_widget()
        layout = QVBoxLayout(self)
        layout.addLayout(header_layout)
        layout.addWidget(self._widget_list)

    def _construct_list_widget(self) -> None:
        """
        Constructs the List of Chats
        """
        self._widget_list = QListWidget()
        for item in self._chats:
            list_item: QListWidgetItem = QListWidgetItem(self._widget_list)
            self._widget_list.addItem(list_item)
            card: ChatCard = ChatCard(item)
            list_item.setSizeHint(card.minimumSizeHint())
            self._widget_list.setItemWidget(list_item, card)

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
        text_input.setFixedHeight(32)
        header_layout = QHBoxLayout()
        header_layout.addWidget(image_button)
        header_layout.addWidget(text_input)
        return header_layout

    def unhide_all(self) -> None:
        """
        Unhides all Widget List Items
        """
        for i, item in enumerate(self._chats):
            self._widget_list.item(i).setHidden(False)

    def _search_chats(self, regex: str) -> None:
        """
        Searches Chats based on Regular Expression

        Parameters
        ----------

        regex: str
             User provied regular expression to use on chats
        """
        self.unhide_all()
        try:
            REGEX: Final[Pattern] = re.compile(regex)
            filtered_indexs = [
                i
                for (i, chat) in enumerate(self._chats)
                if not REGEX.match(chat.other.handle)
            ]
            # Update Model
            for index in filtered_indexs:
                self._widget_list.item(index).setHidden(True)
        except (SyntaxError, re.error):
            pass
