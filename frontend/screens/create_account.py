#!/usr/bin/env python3
from typing import Tuple, Dict
import os
import json

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit
import rsa

from ..components.text_input import TextInput
from .. import requests


class CreateAccount(QMainWindow):
    email_input: QLineEdit
    handle_input: TextInput
    password_input: TextInput
    verify_password_input: TextInput

    def __init__(self, *args, **kwargs):
        super(CreateAccount, self).__init__(*args, **kwargs)
        # TODO: more strict email regex
        self.email_input = TextInput(hint="Email", validator=r".+@.+\.\w{3}")
        self.handle_input = TextInput(hint="Handle")
        self.password_input = TextInput(hint="Password")
        self.verify_password_input = TextInput(hint="Verify Password")
        button = QPushButton("Create Account")
        button.clicked.connect(self._create_account)

        layout = QVBoxLayout()

        layout.addWidget(self.email_input)
        layout.addWidget(self.handle_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.verify_password_input)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    @staticmethod
    def _generate_rsa_keys() -> Tuple[rsa.PublicKey, rsa.PrivateKey]:
        return rsa.newkeys(4096, poolsize=os.cpu_count() or 1)
        # rsa.PrivateKey.save_pkcs1()

    @staticmethod
    def _strip_whitespace(private_key: str) -> str:
        strip_header_footer = private_key[31:-29]
        return "".join(strip_header_footer.split())

    def _create_account(self) -> None:
        (pubkey, privkey) = self._generate_rsa_keys()
        payload: Dict[str, str] = {
            "email": self.email_input.text,
            "handle": self.handle_input.text,
            "password": self.password_input.text,
            "public_key": self._strip_whitespace(pubkey.save_pkcs1().decode()),
        }
        response = requests.post(
            "http://127.0.0.1:8888/create/user", json.dumps(payload)
        )
        print(response)
