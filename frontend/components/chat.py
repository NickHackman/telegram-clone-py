from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from . import USER_ICON


class Chat(QtWidgets.QWidget):
    def __init__(self, values):
        QtWidgets.QWidget.__init__(self)

        name = values["name"]
        date = values["date"]
        message = values["message"]

        self.setStyleSheet("background-color: rgb(23, 33, 43);")
        h_layout = QtWidgets.QHBoxLayout(self)
        h_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        h_layout.setContentsMargins(0, 0, 10, 0)

        icon = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap(USER_ICON)), "", self)
        icon.setEnabled(False)
        icon.setMaximumSize(QtCore.QSize(45, 45))
        icon.setIconSize(QtCore.QSize(45, 45))
        icon.setFlat(True)

        h_layout.addWidget(icon)

        v_layout = QtWidgets.QVBoxLayout()

        inner_h_layout = QtWidgets.QHBoxLayout()
        name_widget = QtWidgets.QLabel(name, self)
        name_widget.setStyleSheet("color: rgb(255, 255, 255)")

        inner_h_layout.addWidget(name_widget)

        date_widget = QtWidgets.QLabel(date, self)
        date_widget.setStyleSheet("color: rgb(255, 255, 255)")
        date_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        date_widget.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )

        inner_h_layout.addWidget(date_widget)
        v_layout.addLayout(inner_h_layout)

        message_widget = QtWidgets.QLabel(message, self)
        message_widget.setStyleSheet("color: rgb(255, 255, 255)")

        v_layout.addWidget(message_widget)
        h_layout.addLayout(v_layout)
