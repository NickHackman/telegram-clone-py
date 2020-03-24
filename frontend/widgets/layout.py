"""
Layout

A wrapper around QVBoxLayout and QHBoxLayout
"""
from enum import Enum
from typing import Union, List

from PyQt5 import QtCore, QtWidgets  # type: ignore


class Direction(Enum):
    """
    Direction of Layout

    Variants
    --------

    Horizontal
          Makes the Layout a QHBoxLayout

    Vertical
          Makes the Layout a QVBoxLayout
    """

    Horizontal = QtWidgets.QHBoxLayout
    Vertical = QtWidgets.QVBoxLayout


class Layout(QtWidgets.QWidget):
    layout: Union[QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout]

    def __init__(
        self,
        *,
        widgets: List[QtWidgets.QWidget] = [],
        direction: Direction = Direction.Horizontal,
        parent: QtCore.QObject = None,
        spacing: int = None
    ):
        """
        Layout

        Wrapper around QVBoxLayout and QHBoxLayout

        Parameters
        ----------

        widgets: List[QtWidgets.QWidget] = []
              List of widgets

        direction: Direction = Direction.Horizontal
              Either a QHBoxLayout or QVBoxLayout

        parent: QtCore.QObject = None
              Parent widget

        spacing: int = None
              Spacing between widgets, default inherits from parent
        """
        super(Layout, self).__init__(parent)
        self.layout = direction.value()
        for widget in widgets:
            widget.setParent(self.layout)
            self.layout.addWidget(widget)
        if spacing:
            self.layout.setSpacing(spacing)
        self.setLayout(self.layout)
