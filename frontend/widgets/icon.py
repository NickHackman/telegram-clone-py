"""
QLabel as an Icon
"""
from typing import Tuple

from PyQt5 import QtCore, QtSvg  # type: ignore

from .qtwidget import QtWidget


class Icon(QtWidget):
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

    icon: QtSvg.QSvgWidget

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
        self.icon = QtSvg.QSvgWidget(icon_path, self)
        self.icon.setMaximumSize(width, height)
        if geometry:
            self.icon.setGeometry(QtCore.QRect(*geometry))
