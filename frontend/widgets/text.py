"""
Text

Wrapper around QLabel
"""
from typing import Tuple

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .alignment import Align


class Text(QtWidgets.QWidget):
    """
    Wrapper around QLabel

    Parameters
    ----------

    text: str
        Text to display

    parent: QtCore.QObject = None
        Parent Widget

    indent: int = 0
        Text indentation

    geometry: Tuple[int, int, int, int] = None
        Location of Widget

    margin: int = 0
        Margins

    align: Align = Align.Left
        Alignment of Text
    """

    label: QtWidgets.QLabel

    def __init__(
        self,
        text: str,
        *,
        parent: QtCore.QObject = None,
        indent: int = 0,
        geometry: Tuple[int, int, int, int] = None,
        margin: int = 0,
        align: Align = Align.Left,
    ):
        super(Text, self).__init__(parent)
        self.label = QtWidgets.QLabel(text, self)
        self.label.setIndent(indent)
        self.label.setMargin(margin)
        self.label.setAlignment(align.value)
