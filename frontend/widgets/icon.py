"""
QLabel as an Icon
"""
from typing import Tuple

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore


class Icon(QtWidgets.QWidget):
    """
    Wrapper around QLabel

    Parameters
    ----------

    icon_path: str
        Path to Icon

    parent: QtCore.QObject = None
        Parent Widget

    width: int = 32
        Width of Icon

    height: int = 32
        Height of Icon

    geometry: Tuple[int, int, int, int] = None
        Location of Widget

    scaled: bool = True
        Whether to scale the image or not
    """

    icon_label: QtWidgets.QLabel

    def __init__(
        self,
        icon_path: str,
        *,
        parent: QtCore.QObject = None,
        width: int = 32,
        height: int = 32,
        geometry: Tuple[int, int, int, int] = None,
        scaled: bool = True,
    ):
        super(Icon, self).__init__(parent)
        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setPixmap(QtGui.QPixmap(icon_path))
        self.icon_label.setScaledContents(scaled)
        self.icon_label.setStyleSheet(f"width: {width};\n" f"height: {height};")
        if geometry:
            self.icon_label.setGeometry(*geometry)
