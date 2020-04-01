from pathlib import Path
import os
import json
from typing import Dict, Any

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
import rsa

from .. import requests
from . import Router, TELEGRAM_ICON, BACKARROW_ICON


class Login(object):
    def __init__(self, router: Router):
        self.router = router

    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(474, 608)
        Login.setStyleSheet("background-color: rgb(14, 22, 33);")
        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 360, 351, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setStyleSheet("color: rgb(99, 111, 122);")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setStyleSheet("color: rgb(99, 111, 122);")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.password_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.password_input.setInputMethodHints(
            QtCore.Qt.ImhHiddenText
            | QtCore.Qt.ImhNoAutoUppercase
            | QtCore.Qt.ImhNoPredictiveText
            | QtCore.Qt.ImhSensitiveData
        )
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("")
        self.password_input.setObjectName("password_input")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.password_input
        )
        self.email_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.email_input.setAutoFillBackground(False)
        self.email_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.email_input.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.email_input.setObjectName("email_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.email_input)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 490, 351, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.login_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.login_button.setStyleSheet(
            "color: rgb(99, 111, 122);\n" "background-color: rgb(23, 33, 43);"
        )
        self.login_button.setAutoDefault(False)
        self.login_button.setDefault(False)
        self.login_button.setFlat(False)
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(lambda: self._login(Login))
        self.horizontalLayout.addWidget(self.login_button)
        self.create_account_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.create_account_button.setStyleSheet(
            "color: rgb(99, 111, 122);\n" "background-color: rgb(23, 33, 43);"
        )
        self.create_account_button.setObjectName("create_account_button")
        self.create_account_button.clicked.connect(lambda: self._create_account(Login))
        self.horizontalLayout.addWidget(self.create_account_button)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 90, 211, 181))
        self.label_3.setStyleSheet("width: 25;\n" "height: 25;")
        self.label_3.setPixmap(QtGui.QPixmap(TELEGRAM_ICON))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.error_message = QtWidgets.QLabel(self.centralwidget)
        self.error_message.setGeometry(QtCore.QRect(60, 440, 351, 16))
        self.error_message.setStyleSheet("color: rgb(255, 2, 6);")
        self.error_message.setText("")
        self.error_message.setObjectName("error_message")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(-10, 10, 81, 23))
        self.back_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(BACKARROW_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(24, 24))
        self.back_button.setFlat(True)
        self.back_button.clicked.connect(self._go_back)
        self.back_button.setObjectName("back_button")
        Login.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Login)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 20))
        self.menubar.setObjectName("menubar")
        Login.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Login)
        self.statusbar.setObjectName("statusbar")
        Login.setStatusBar(self.statusbar)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        Login.setTabOrder(self.email_input, self.password_input)
        Login.setTabOrder(self.password_input, self.login_button)
        Login.setTabOrder(self.login_button, self.create_account_button)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Telegram-clone-py Login"))
        self.label.setText(_translate("Login", "Email"))
        self.label_2.setText(_translate("Login", "Password"))
        self.login_button.setText(_translate("Login", "Login"))
        self.create_account_button.setText(_translate("Login", "Create Account"))

    def _login(self, window) -> None:
        """
        Sends POST request to server
        """
        self.login_button.setEnabled(False)
        email: str = self.email_input.text()
        password: str = self.password_input.text()
        if not email or not password:
            self.error_message.setText("Email and password are required")
            self.login_button.setEnabled(True)
            return

        payload: Dict[str, Any] = {"email": email, "password": password}
        url: str = self.router.state["url"]
        response = requests.post(f"{url}/login", json.dumps(payload))
        if response.json["status"] == "success":
            data: Dict[str, Any] = response.json["response"]
            self.router.set_state("jwt", data["token"])
            self.router.set_state("public_key", data["public_key"])
            self.router.set_state("handle", data["handle"])
            self.router.set_state("privkey", self._load_privkey(data["handle"]))
            self.router.push("/main", window)
        else:
            self.error_message.setText(response.json["response"])
            self.login_button.setEnabled(True)

    @staticmethod
    def _load_privkey(handle: str) -> rsa.PrivateKey:
        PATH: str = f"{Path(__file__).parent.parent.parent.absolute()}{os.sep}{handle}_privkey.pem"
        with open(PATH, "r") as file:
            data = file.read()
        return rsa.PrivateKey.load_pkcs1(data)

    def _create_account(self, window) -> None:
        """
        Pushes onto the Router the CreateAccount Screen
        """
        self.router.push("/create/account", window)

    def _go_back(self) -> None:
        """
        Pops one screen off the Stack

        Theoretically going back to the ConnectToServer Screen
        """
        self.router.pop()
