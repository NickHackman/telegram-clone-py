from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from . import EMOTE_ICON, SEND_ICON, SEARCH_ICON


class ChatWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(984, 718)
        Form.setStyleSheet(
            "background-color: rgb(14, 22, 33); \n"
            "QMainWindow::separator { width: 0; height: 0; }"
        )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalWidget = QtWidgets.QWidget(Form)
        self.horizontalWidget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.name = QtWidgets.QLabel(self.horizontalWidget)
        self.name.setStyleSheet("color: rgb(255, 255, 255);")
        self.name.setText("")
        self.name.setObjectName("name")
        self.verticalLayout_3.addWidget(self.name)
        self.last_seen = QtWidgets.QLabel(self.horizontalWidget)
        self.last_seen.setStyleSheet("color: rgb(79, 95, 112);")
        self.last_seen.setText("")
        self.last_seen.setIndent(-1)
        self.last_seen.setObjectName("last_seen")
        self.verticalLayout_3.addWidget(self.last_seen)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.pushButton = QtWidgets.QPushButton(self.horizontalWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(SEARCH_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(24, 24))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget(self.horizontalWidget)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_line = QtWidgets.QLineEdit(self.widget)
        self.message_line.setMinimumSize(QtCore.QSize(0, 32))
        self.message_line.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(36, 47, 61);\n"
            "border-radius: 2px;"
        )
        self.message_line.setObjectName("message_line")
        self.horizontalLayout.addWidget(self.message_line)
        self.emoji_button = QtWidgets.QPushButton(self.widget)
        self.emoji_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(EMOTE_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.emoji_button.setIcon(icon1)
        self.emoji_button.setIconSize(QtCore.QSize(24, 24))
        self.emoji_button.setFlat(True)
        self.emoji_button.setObjectName("emoji_button")
        self.horizontalLayout.addWidget(self.emoji_button)
        self.send_button = QtWidgets.QPushButton(self.widget)
        self.send_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(SEND_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.send_button.setIcon(icon2)
        self.send_button.setIconSize(QtCore.QSize(24, 24))
        self.send_button.setFlat(True)
        self.send_button.setObjectName("send_button")
        self.horizontalLayout.addWidget(self.send_button)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.message_line.setPlaceholderText(_translate("Form", "Send a message..."))
