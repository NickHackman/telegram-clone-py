import re
from typing import List, Pattern, Any, Dict
from threading import Thread
from datetime import datetime
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from . import Router, MENU_ICON
from ..components.chat import ChatWidget
from ..components.chat_window import ChatWindow

from .. import requests
from ..components.chat_list_widget_item import ChatListWidgetItem

from ..models import Chat
from ..models.user import User


class Main(QtCore.QObject):
    users: List[User]
    chats: List[Chat]
    search_signal = QtCore.pyqtSignal(object)

    def __init__(self, router: Router):
        super(Main, self).__init__(None)
        self.users = []
        self.chats = []
        self.router = router

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 764)
        MainWindow.setStyleSheet("background-color: rgb(14, 22, 33);")
        MainWindow.setStatusBar(None)
        self.central_widget = QtWidgets.QWidget()
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.central_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        MainWindow.setCentralWidget(self.central_widget)
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
        self.dockWidgetContents.setContentsMargins(5, 0, 0, 0)
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
        self.search_input = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.search_input.setEnabled(True)
        self.search_input.setMinimumSize(QtCore.QSize(0, 32))
        self.search_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(36, 47, 61);\n"
            "border-radius: 2px;"
        )
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setObjectName("lineEdit")
        self.search_input.editingFinished.connect(lambda: self._search())
        self.horizontalLayout.addWidget(self.search_input)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(self.dockWidgetContents)
        self.listWidget.itemClicked.connect(
            lambda item: self._change_main(item, MainWindow)
        )
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dockWidget.setWidget(self.dockWidgetContents)
        thread = Thread(target=self._update_chats, daemon=True)
        thread.start()
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        timer = QtCore.QTimer(MainWindow)
        timer.timeout.connect(self._update_list)
        timer.setInterval(500)
        timer.start()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_input.setPlaceholderText(_translate("MainWindow", " Search"))

    def _change_main(
        self, item: ChatListWidgetItem, window: QtWidgets.QMainWindow
    ) -> None:
        # Subclass QListWidgetItem to allow for data then pass into ChatWindow
        central_widget = QtWidgets.QWidget()
        chat_window = ChatWindow(item.chat, item.state)
        chat_window.setupUi(central_widget)
        window.setCentralWidget(central_widget)

    def _query_users(self, regex: Pattern[str]):
        """
        Queries Users then filters based on regex

        Parameters
        ----------

        regex: Pattern[str]
             Pattern to filter by

        Returns
        -------

        List[Any]
        new list of Chats
        """
        response = requests.get(f"{self.router.state['url']}/users")
        response.raise_for_status()
        self.users = [
            Chat(User(user["handle"], user["public_key"], user["bio"]), [])
            for user in response.json["response"]
            if regex.match(user["handle"])
        ]
        print(self.users)

    def _update_list(self) -> None:
        """
        Updates the list of chats shown with the new results

        Parameters
        ----------

        new_list: List[Any]
              New list of chats
        """
        self.listWidget.clear()
        for user in self.users:
            list_item = ChatListWidgetItem(user, self.router.state, self.listWidget)
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, ChatWidget(user))

    def _update_chats(self) -> None:
        state: Dict[str, Any] = self.router.state
        while True:
            time.sleep(3)
            response = requests.get(
                f"{state['url']}/messages/{state['handle']}/{state['jwt']}"
            )
            print(response.json)

    def _search(self) -> None:
        """
        Performs Search query

        Runs the HTTP Request and filtering in the background
        """
        try:
            regex: Pattern[str] = re.compile(self.search_input.text())
            thread = Thread(target=self._query_users, args=[regex])
            thread.start()
        except re.error:
            pass
