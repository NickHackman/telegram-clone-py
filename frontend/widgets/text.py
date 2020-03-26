"""
Text

Wrapper around QLabel
"""
from typing import Tuple

from PyQt5 import QtCore, QtWidgets  # type: ignore

from .alignment import VerticalAlign, HorizontalAlign
from .qtwidget import QtWidget


class Text(QtWidget):
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
        h_align: HorizontalAlign = HorizontalAlign.Left,
        v_align: VerticalAlign = VerticalAlign.BaseLine
    ):
        super(Text, self).__init__(parent)
        self.label = QtWidgets.QLabel(text)
        self.label.setIndent(indent)
        self.label.setMargin(margin)
        self.label.setAlignment(h_align.value | v_align.value)
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        if geometry:
            self.label.setGeometry(QtCore.QRect(*geometry))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_text(self, text: str) -> None:
        """
        Sets Label's Text

        Parameters
        ----------

        text: str
              New string for label
        """
        self.label.setText(text)
