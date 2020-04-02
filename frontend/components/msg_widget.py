from PyQt5 import QtCore, QtGui, QtWidgets

from ..models.message import Message


class MessageWidget(object):
    def __init__(self, message: Message):
        self.msg = message

    def setupUi(self, MessageWidget):
        MessageWidget.setObjectName("MessageWidget")
        MessageWidget.resize(534, 112)
        MessageWidget.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MessageWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sender_name = QtWidgets.QLabel(MessageWidget)
        self.sender_name.setMinimumSize(QtCore.QSize(0, 16))
        self.sender_name.setStyleSheet("color: rgb(250, 163, 87);")
        self.sender_name.setText(self.msg.sender)
        self.sender_name.setObjectName("sender_name")
        self.verticalLayout.addWidget(self.sender_name)
        self.message = QtWidgets.QTextEdit(MessageWidget)
        self.message.setEnabled(True)
        self.message.setText(self.msg.message)
        self.message.setMinimumHeight(32)
        self.message.setStyleSheet("color: rgb(255, 255, 255);")
        self.message.setReadOnly(True)
        self.message.setObjectName("message")
        self.verticalLayout.addWidget(self.message)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(MessageWidget)
        QtCore.QMetaObject.connectSlotsByName(MessageWidget)

    def retranslateUi(self, MessageWidget):
        _translate = QtCore.QCoreApplication.translate
        MessageWidget.setWindowTitle(_translate("MessageWidget", "Form"))
