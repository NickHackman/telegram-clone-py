from PyQt5 import QtWidgets  # type: ignore

from .qtwidget import QtWidget


class Spacer(QtWidget):
    """
    Spacer

    Parameters
    ----------

    width: int
          Width of spacer

    height: int
          Height of spacer

    parent: QtWidgets.QWidget = None
          Parent Widget
    """

    def __init__(self, width: int, height: int, *, parent: QtWidgets.QWidget = None):
        super(Spacer, self).__init__(parent)
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        spacer: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(width, height)
        layout.addItem(spacer)
        self.setLayout(layout)
