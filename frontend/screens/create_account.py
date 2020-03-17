#!/usr/bin/env python3
from typing import Tuple, Dict, Any
import os
import json

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget  # type: ignore
import rsa  # type: ignore

from ..components.text_input import TextInput
from .. import requests


class CreateAccount(QMainWindow):
    email_input: TextInput
    handle_input: TextInput
    password_input: TextInput
    verify_password_input: TextInput

    def __init__(self, *args, **kwargs):
        """
        Consructs CreateAccount screen

        Fields
        ------

        email: takes valid email addresses
        handle: takes valid Handles
        password: takes valid passwords
        verify password: takes valid passwords

        Buttons
        -------

        create account: generates RSA key and POSTs to server,
          does nothing if password != verify password
        """
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
        """
        Generates RSA keys with all CPUs or 1

        Returns
        -------

        Tuple[rsa.PublicKey, rsa.PrivateKey]
              Tuple of Public and Private keys
        """
        return rsa.newkeys(4096, poolsize=os.cpu_count() or 1)
        # TODO: Save Privatekey to file
        # via rsa.PrivateKey.save_pkcs1()

    @staticmethod
    def _strip_whitespace(public_key: str) -> str:
        """
        Removes Header and Footer of PEM RSA Key then strips newlines

        Parameters
        ----------

        public_key: str
             string to strip

        Returns
        -------

        str
             Stripped string
        """
        strip_header_footer = public_key[31:-29]
        return "".join(strip_header_footer.split())

    def _create_account(self) -> None:
        """
        Creates an Account by generating an RSA and creating an account Server side
        """
        password: str = self.password_input.text
        verify_password: str = self.verify_password_input.text
        email = self.email_input.text
        handle = self.handle_input.text

        if password != verify_password:
            return

        (pubkey, privkey) = self._generate_rsa_keys()
        payload: Dict[str, Any] = {
            "email": email,
            "handle": handle,
            "password": password,
            "public_key": self._strip_whitespace(pubkey.save_pkcs1().decode()),
        }
        response = requests.post(
            "http://127.0.0.1:8888/create/user", json.dumps(payload)
        )
        print(response)
