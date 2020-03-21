from PyQt5 import QtCore, QtGui, QtWidgets

from . import Router, MENU_ICON
from ..components.chat import Chat


items = [
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Erik", "date": "Now", "message": "Erik: I use Arch Btw"},
    {"name": "Sarah", "date": "Now", "message": "You: Hi"},
]


class Main(object):
    def __init__(self, router: Router):
        self.router = router

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 764)
        MainWindow.setStyleSheet("background-color: rgb(14, 22, 33);")
        MainWindow.setStatusBar(None)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        MainWindow.setCentralWidget(self.centralwidget)
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
        self.listWidget.itemClicked.connect(Chat.selected)
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
