import re
from typing import List, Pattern

from PyQt5 import QtCore, QtGui, QtWidgets

from . import Router, MENU_ICON
from ..components.chat import Chat
from ..components.chat_window import ChatWindow

from .. import requests
from ..thread import QtThread


items = [
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Sarah", "date": "Now", "message": "You: I love you"},
]


class Main(object):
    def __init__(self, router: Router):
        self.router = router
        self.chats = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 764)
        MainWindow.setStyleSheet("background-color: rgb(14, 22, 33);")
        MainWindow.setStatusBar(None)
        central_widget = QtWidgets.QWidget()
        chat_window = ChatWindow()
        chat_window.setupUi(central_widget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(central_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        MainWindow.setCentralWidget(central_widget)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget.setWindowTitle("")
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget(self.dockWidget))
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton.setStyleSheet("padding: 10px;")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(MENU_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(24, 24))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 32))
        self.lineEdit.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(36, 47, 61);\n"
            "border-radius: 2px;"
        )
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(self.dockWidgetContents)
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        for item in items:
            list_item = QtWidgets.QListWidgetItem(self.listWidget)
            widget = QtWidgets.QWidget()
            chat = Chat(item)
            chat.setupUi(widget)
            list_item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, widget)
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", " Search"))

    def search_update_cb(self, regex: Pattern[str]) -> None:
        url: str = self.router.state["url"]
        response = requests.get(f"{url}/users")
        users: List[str] = response.json["response"]
        print(users)
        for user in users:
            if not regex.match(user):
                continue
            list_item = QtWidgets.QListWidgetItem(self.listWidget)
            widget = QtWidgets.QWidget()
            chat = Chat({"name": user, "date": "", "message": ""})
            chat.setupUi(widget)
            list_item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, widget)

    def _search(self, text: str) -> None:
        try:
            REGEX = re.compile(text)
        except re.error:
            return
        thread = Thread(target=lambda: self.search_update_cb(REGEX))
        thread.start()
