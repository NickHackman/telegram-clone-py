#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget  # type: ignore

from ..components.text_input import TextInput, InputType
from .. import requests


class ConnectToServer(QMainWindow):
    def __init__(self, *args, **kwargs):
        """
        Consructs ConnectToServer screen

        Fields
        ------

        url: takes website url
        port: Port number on server

        Buttons
        -------

        Connect: Asks the server if it's a telegram-clone-server
        """
        super(ConnectToServer, self).__init__(*args, **kwargs)
        self.url_input = TextInput(hint="Server URL", validator=r"http(s)?://[\w\d\.]+")
        self.port_input = TextInput(hint="Server port number", validator=r"\d+")
        button = QPushButton("Connect")
        button.clicked.connect(self._ask_server)

        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.port_input)
        layout.addWidget(button)

        widget: QWidget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _ask_server(self) -> None:
        """
        Sends GET HTTP Request to Server
        """
        url = self.url_input.text
        port: int = int(self.port_input.text)
        try:
            response = requests.get(f"{url}:{port}/is/telegram-clone-server")
            print(response)
        except Exception as err:
            pass
