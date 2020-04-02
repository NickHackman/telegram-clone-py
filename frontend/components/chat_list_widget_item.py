from typing import Dict, Any

from PyQt5 import QtCore, QtGui, QtWidgets

from ..models import Chat


class ChatListWidgetItem(QtWidgets.QListWidgetItem):
    """
    Construct a ChatListWidgetItem

    wrapper around QListWidgetItem that holds data for a Chat

    Parameters
    ----------

    chat: Chat
          Chat data

    parent: QtWidgets.QListWidget
          parent QListWidget
    """

    chat: Chat
    state: Dict[str, Any]

    def __init__(
        self, chat: Chat, state: Dict[str, Any], parent: QtWidgets.QListWidget
    ):
        super(ChatListWidgetItem, self).__init__(parent, 1000)
        self.chat = chat
        self.state = state
