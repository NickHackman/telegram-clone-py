import json
import os
from typing import Dict, Any, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets  # type:ignore
import rsa  # type: ignore

from .. import requests
from . import Router, TELEGRAM_ICON, BACKARROW_ICON


class CreateAccount(object):
    def __init__(self, router: Router):
        self.router = router

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(477, 609)
        MainWindow.setStyleSheet("background-color: rgb(14, 22, 33)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 80, 211, 181))
        self.label_3.setStyleSheet("width: 25;\n" "height: 25;")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(TELEGRAM_ICON))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 320, 391, 154))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setStyleSheet("color: rgb(99, 111, 122);")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
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
            2, QtWidgets.QFormLayout.FieldRole, self.password_input
        )
        self.verify_password_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.verify_password_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.verify_password_input.setInputMethodHints(
            QtCore.Qt.ImhHiddenText
            | QtCore.Qt.ImhNoAutoUppercase
            | QtCore.Qt.ImhNoPredictiveText
            | QtCore.Qt.ImhSensitiveData
        )
        self.verify_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verify_password_input.setPlaceholderText("")
        self.verify_password_input.setObjectName("verify_password_input")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.verify_password_input
        )
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setStyleSheet("color: rgb(99, 111, 122);")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setStyleSheet("color: rgb(99, 111, 122);")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setStyleSheet("color: rgb(99, 111, 122);")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.handle_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.handle_input.setAutoFillBackground(False)
        self.handle_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.handle_input.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.handle_input.setObjectName("handle_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.handle_input)
        self.create_account_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_account_button.setGeometry(QtCore.QRect(180, 520, 124, 23))
        self.create_account_button.setStyleSheet(
            "color: rgb(99, 111, 122);\n" "background-color: rgb(23, 33, 43);"
        )
        self.create_account_button.setObjectName("create_account_button")
        self.create_account_button.clicked.connect(
            lambda: self._create_account(MainWindow)
        )
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(-10, 10, 81, 23))
        self.back_button.setText("")
        self.back_button.clicked.connect(self._go_back)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(BACKARROW_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(24, 24))
        self.back_button.setFlat(True)
        self.back_button.setObjectName("back_button")
        self.error_message = QtWidgets.QLabel(self.centralwidget)
        self.error_message.setGeometry(QtCore.QRect(66, 490, 381, 20))
        self.error_message.setStyleSheet("color: rgb(255, 0, 4);")
        self.error_message.setText("")
        self.error_message.setObjectName("error_message")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 477, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.email_input, self.handle_input)
        MainWindow.setTabOrder(self.handle_input, self.password_input)
        MainWindow.setTabOrder(self.password_input, self.verify_password_input)
        MainWindow.setTabOrder(self.verify_password_input, self.create_account_button)
        MainWindow.setTabOrder(self.create_account_button, self.back_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Email"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.label_4.setText(_translate("MainWindow", "Verify Password"))
        self.label_5.setText(_translate("MainWindow", "Handle"))
        self.create_account_button.setText(_translate("MainWindow", "Create Account"))

    @staticmethod
    def _generate_rsa_keys() -> Tuple[rsa.PublicKey, rsa.PrivateKey]:
        return rsa.newkeys(4096, poolsize=os.cpu_count() or 1)

    def _create_account(self, window) -> None:
        """
        Creates an Account with provided fields
        """
        self.create_account_button.setEnabled(False)
        email: str = self.email_input.text()
        handle: str = self.handle_input.text()
        password: str = self.password_input.text()
        password_verify: str = self.verify_password_input.text()
        if not email or not handle or not password:
            self.error_message.setText("All fields are required")
            self.create_account_button.setEnabled(True)
            return

        if password != password_verify:
            self.error_message.setText("Password and Verify password are different")
            self.create_account_button.setEnabled(True)
            return

        (pubkey, privkey) = self._generate_rsa_keys()
        payload: Dict[str, Any] = {
            "email": email,
            "handle": handle,
            "password": password,
            "public_key": pubkey,
        }

        url: str = self.router.state["url"]
        response = requests.post(f"{url}/create/user", json.dumps(payload))
        if response.json["status"] == "success":
            self.router.push("/login", window)
        else:
            self.error_message.setText("Error")
            self.create_account_button.setEnabled(True)

    def _go_back(self) -> None:
        self.router.pop()
