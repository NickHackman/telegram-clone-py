from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .. import requests
from ..requests.response import HTTPError
from . import Router, TELEGRAM_ICON, BACKARROW_ICON


class ConnectToServer(object):
    def __init__(self, router: Router):
        self.router = router

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(482, 620)
        MainWindow.setStyleSheet("background-color: rgb(14, 22, 33);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 380, 351, 81))
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
        self.url_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.url_input.setAutoFillBackground(False)
        self.url_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.url_input.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.url_input.setObjectName("url_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.url_input)
        self.port_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.port_input.setStyleSheet(
            "background: rgb(23, 33, 43);\n"
            "border-color: rgb(16, 25, 33);\n"
            "color: rgb(255, 255, 255);"
        )
        self.port_input.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.port_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.port_input.setPlaceholderText("")
        self.port_input.setObjectName("port_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.port_input)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 100, 211, 181))
        self.label_3.setStyleSheet("width: 25;\n" "height: 25;")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(TELEGRAM_ICON))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(180, 520, 124, 23))
        self.connect_button.clicked.connect(lambda: self._connect(MainWindow))
        self.connect_button.setStyleSheet(
            "color: rgb(99, 111, 122);\n" "background-color: rgb(23, 33, 43);"
        )
        self.connect_button.setObjectName("connect_button")
        self.error_message = QtWidgets.QLabel(self.centralwidget)
        self.error_message.setGeometry(QtCore.QRect(60, 470, 351, 20))
        self.error_message.setStyleSheet("color: rgb(255, 2, 6);")
        self.error_message.setText("")
        self.error_message.setObjectName("error_message")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "URL"))
        self.label_2.setText(_translate("MainWindow", "Port"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))

    def _connect(self, window) -> None:
        """
        Attempts to connect to Telegram Clone Server

        On success switches to login screen
        On Failure sets error message
        """
        url: str = self.url_input.text()
        port: int = int(self.port_input.text())

        try:
            response = requests.get(f"{url}:{port}/is/telegram-clone-server")
            response.raise_for_status()
            if response.json["status"] == "success":
                self.router.set_state("url", f"{url}:{port}")
                self.router.push("/login", window)
            else:
                self.error_message.setText("Not a valid Telegram-clone-server")
        except HTTPError:
            self.error_message.setText("Not a valid Telegram-clone-server")
