from PyQt5 import QtCore, QtGui, QtWidgets

from . import USER_ICON


class Chat(object):
    def __init__(self, values):
        self._name = values["name"]
        self._date = values["date"]
        self._message = values["message"]

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setStyleSheet("background-color: rgb(23, 33, 43);")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setEnabled(False)
        self.pushButton.setMaximumSize(QtCore.QSize(45, 45))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(USER_ICON), QtGui.QIcon.Normal, QtGui.QIcon.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(45, 45))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.name = QtWidgets.QLabel(Form)
        self.name.setStyleSheet("color: rgb(255, 255, 255);")
        self.name.setObjectName("name")
        self.name.setText(self._name)
        self.horizontalLayout_3.addWidget(self.name)
        self.date = QtWidgets.QLabel(Form)
        self.date.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.date.setStyleSheet("color: rgb(255, 255, 255);")
        self.date.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.date.setObjectName("date")
        self.date.setText(self._date)
        self.horizontalLayout_3.addWidget(self.date)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.message = QtWidgets.QLabel(Form)
        self.message.setStyleSheet("color: rgb(255, 255, 255);")
        self.message.setObjectName("message")
        self.message.setText(self._message)
        self.verticalLayout.addWidget(self.message)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
