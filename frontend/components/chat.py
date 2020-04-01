from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from . import USER_ICON
from ..models import Chat
from ..models.message import Message


class ChatWidget(QtWidgets.QWidget):
    chat: Chat

    def __init__(self, chat: Chat):
        QtWidgets.QWidget.__init__(self)

        self.setStyleSheet("background-color: rgb(23, 33, 43);")
        h_layout = QtWidgets.QHBoxLayout(self)
        h_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        h_layout.setContentsMargins(0, 0, 10, 0)

        icon = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap(USER_ICON)), "", self)
        icon.setEnabled(False)
        icon.setMaximumSize(QtCore.QSize(45, 45))
        icon.setIconSize(QtCore.QSize(45, 45))
        icon.setFlat(True)

        h_layout.addWidget(icon)

        v_layout = QtWidgets.QVBoxLayout()

        inner_h_layout = QtWidgets.QHBoxLayout()
        name_widget = QtWidgets.QLabel(chat.other.handle, self)
        name_widget.setStyleSheet("color: rgb(255, 255, 255)")

        inner_h_layout.addWidget(name_widget)

        last_message: Optional[Message] = None
        try:
            last_message = chat.messages[-1]
        except IndexError:
            last_message = Message("", "", "", "Never")
        date_widget = QtWidgets.QLabel(last_message.date, self)
        date_widget.setStyleSheet("color: rgb(255, 255, 255)")
        date_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        date_widget.setAlignment(QtCore.Qt.AlignRight)
        date_widget.setAlignment(QtCore.Qt.AlignVCenter)

        inner_h_layout.addWidget(date_widget)
        v_layout.addLayout(inner_h_layout)

        message: str = f"{last_message.sender}: {last_message.message}" if last_message.message else ""
        message_widget = QtWidgets.QLabel(message, self)
        message_widget.setStyleSheet("color: rgb(255, 255, 255)")

        v_layout.addWidget(message_widget)
        h_layout.addLayout(v_layout)
