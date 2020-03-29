import re
from typing import List, Pattern, Any

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from . import Router, MENU_ICON
from ..components.chat import Chat
from ..components.chat_window import ChatWindow

from .. import requests
from ..thread import QtThread


class Main(QtCore.QObject):
    search_signal = QtCore.pyqtSignal(object)

    def __init__(self, router: Router):
        QtCore.QObject.__init__(self)
        self.router = router

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 764)
        MainWindow.setStyleSheet(
            "background-color: rgb(14, 22, 33);\n"
            "QMainWindow::separator { width: 0; height: 0; }"
        )
        MainWindow.setStatusBar(None)
        central_widget = QtWidgets.QWidget()
        chat_window = ChatWindow()
        chat_window.setupUi(central_widget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(central_widget)
        self.verticalLayout_4.setContentsMargins(-10, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        MainWindow.setCentralWidget(central_widget)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setStyleSheet("background-color: rgb(23, 33, 43);\n")
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
        self.search_input = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.search_input.setEnabled(True)
        self.search_input.editingFinished.connect(lambda: self._search())
        self.search_input.setMinimumSize(QtCore.QSize(0, 32))
        self.search_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(36, 47, 61);\n"
            "border-radius: 2px;"
        )
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setObjectName("search_input")
        self.horizontalLayout.addWidget(self.search_input)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(self.dockWidgetContents)
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_input.setPlaceholderText(_translate("MainWindow", " Search"))

    def _query_users(self, regex: Pattern[str]) -> List[Any]:
        url: str = self.router.state["url"]
        response = requests.get(f"{url}/users")
        response.raise_for_status()
        users = [
            {"name": user, "date": "", "message": ""}
            for user in response.json["response"]
        ]
        return users

    def _update_list(self, new_list: List[Any]) -> None:
        self.listWidget.clear()
        for item in new_list:
            list_item = QtWidgets.QListWidgetItem(self.listWidget)
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, Chat(item))

    def _search(self) -> None:
        try:
            regex: Pattern[str] = re.compile(self.search_input.text())
            thread = QtThread(self._query_users, self.search_signal, regex)
            thread.finished.connect(self._update_list)
            thread.start()
        except re.error:
            pass
