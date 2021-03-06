import time
from typing import Dict, Any
import json
import binascii
from threading import Thread

import rsa  # type: ignore
from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .. import requests
from . import EMOTE_ICON, SEND_ICON, SEARCH_ICON
from ..models import Chat
from .msg_widget import MessageWidget


class ChatWindow(QtCore.QObject):
    send_signal = QtCore.pyqtSignal(object)
    recv_signal = QtCore.pyqtSignal(object)

    def __init__(self, chat: Chat, state: Dict[str, Any]):
        super(ChatWindow, self).__init__()
        self.chat = chat
        self.state = state

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(984, 718)
        Form.setStyleSheet("background-color: rgb(14, 22, 33);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalWidget = QtWidgets.QWidget(Form)
        self.horizontalWidget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.name = QtWidgets.QLabel(self.horizontalWidget)
        self.name.setStyleSheet("color: rgb(255, 255, 255);")
        self.name.setText(self.chat.other.handle)
        self.name.setObjectName("name")
        self.verticalLayout_3.addWidget(self.name)
        self.last_seen = QtWidgets.QLabel(self.horizontalWidget)
        self.last_seen.setStyleSheet("color: rgb(79, 95, 112);")
        self.last_seen.setText("Never")
        self.last_seen.setIndent(-1)
        self.last_seen.setObjectName("last_seen")
        self.verticalLayout_3.addWidget(self.last_seen)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.pushButton = QtWidgets.QPushButton(self.horizontalWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(SEARCH_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(24, 24))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget(self.horizontalWidget)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setSpacing(10)
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_line = QtWidgets.QLineEdit(self.widget)
        self.message_line.setMinimumSize(QtCore.QSize(0, 32))
        self.message_line.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(36, 47, 61);\n"
            "border-radius: 2px;"
        )
        self.message_line.setObjectName("message_line")
        self.message_line.returnPressed.connect(lambda: self._send_message())
        self.horizontalLayout.addWidget(self.message_line)
        self.emoji_button = QtWidgets.QPushButton(self.widget)
        self.emoji_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(EMOTE_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.emoji_button.setIcon(icon1)
        self.emoji_button.setIconSize(QtCore.QSize(24, 24))
        self.emoji_button.setFlat(True)
        self.emoji_button.setObjectName("emoji_button")
        self.horizontalLayout.addWidget(self.emoji_button)
        self.send_button = QtWidgets.QPushButton(self.widget)
        self.send_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(SEND_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.send_button.setIcon(icon2)
        self.send_button.setIconSize(QtCore.QSize(24, 24))
        self.send_button.setFlat(True)
        self.send_button.clicked.connect(lambda: self._send_message())
        self.send_button.setObjectName("send_button")
        self.horizontalLayout.addWidget(self.send_button)
        self.verticalLayout.addWidget(self.widget)
        timer = QtCore.QTimer(Form)
        timer.timeout.connect(self._update_list)
        timer.setInterval(1500)
        timer.start()
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.message_line.setPlaceholderText(_translate("Form", "Send a message..."))

    def _update_list(self) -> None:
        self.listWidget.clear()
        for msg in self.state["chat"][self.chat.other.handle].messages:
            list_item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(list_item)
            widget = QtWidgets.QWidget()
            widget_class = MessageWidget(msg)
            widget_class.setupUi(widget)
            list_item.setSizeHint(widget.sizeHint())
            self.listWidget.setItemWidget(list_item, widget)

    def _send_message_to_server(self, message: str) -> None:
        sender_public_key = rsa.PublicKey.load_pkcs1(self.state["public_key"].encode())
        if self.chat.other.public_key:
            reciever_public_key = rsa.PublicKey.load_pkcs1(
                self.chat.other.public_key.encode()
            )
        else:
            reciever_public_key = rsa.PublicKey.load_pkcs1(
                requests.get(f"{self.state['url']}/user/{self.chat.other.handle}").json[
                    "response"
                ]["public_key"]
            )
        payload: Dict[str, Any] = {
            "sender": self.state["handle"],
            "reciever": self.chat.other.handle,
            "sender_message": binascii.b2a_base64(
                rsa.encrypt(message.encode("utf-8"), sender_public_key)
            ).decode(),
            "reciever_message": binascii.b2a_base64(
                rsa.encrypt(message.encode("utf-8"), reciever_public_key)
            ).decode(),
        }
        response = requests.post(
            f"{self.state['url']}/message/{self.state['jwt']}", json.dumps(payload),
        )

    def _send_message(self) -> None:
        thread = Thread(
            target=self._send_message_to_server, args=[self.message_line.text()]
        )
        thread.start()
        self.message_line.clear()
