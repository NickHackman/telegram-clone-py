#!/usr/bin/env python3
from typing import Dict
import json

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from ..components.text_input import TextInput
from .. import requests


class Login(QMainWindow):
    email_input: TextInput
    password_input: TextInput

    def __init__(self, *args, **kwargs):
        """
        Constructs Login screen

        Fields
        ------

        email: takes valid email address
        password: takes valid password

        Buttons
        -------

        Login: POSTs to Server
        """
        super(Login, self).__init__(*args, **kwargs)
        self.email_input = TextInput(hint="Email", validator=r".+@.+\.\w{3}")
        self.password_input = TextInput(hint="Password")
        button: QPushButton = QPushButton("Login")
        button.clicked.connect(self._login)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button)

        widget: QWidget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _login(self) -> None:
        """
        Sends POST request to server
        """
        email = self.email_input.text

        payload: Dict[str, Any] = {
            "password": self.password_input.text,
        }
        response = requests.post(
            f"http://127.0.0.1:8888/login/{email}", json.dumps(payload)
        )
        print(response)
