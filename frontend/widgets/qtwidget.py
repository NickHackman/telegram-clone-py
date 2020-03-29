"""
Base QtWidget

Sets base functionality of all other widgets
"""
from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore


class QtWidget(QtWidgets.QWidget):
    """
    Base QtWidget

    Parameters
    ----------

    parent: QtWidgets.QObject = None
         Parent widget
    """

    def __init__(self, parent: QtCore.QObject = None):
        super(QtWidget, self).__init__(parent)

    def set_parent(self, parent: QtCore.QObject) -> None:
        """
        Sets Parent Widget

        Parameters
        ----------

        parent: QtCore.QObject
              Parent Widget
        """
        self.setParent(parent)
