"""
Layout

A wrapper around QVBoxLayout and QHBoxLayout
"""
from enum import Enum
from typing import List, Union, Tuple

from PyQt5 import QtCore, QtWidgets  # type: ignore

from .qtwidget import QtWidget
from .alignment import HorizontalAlign, VerticalAlign


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


class Layout(QtWidget):
    layout: Union[QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout]

    def __init__(
        self,
        *,
        widgets: List[QtWidgets.QWidget] = [],
        direction: Direction = Direction.Vertical,
        v_align: VerticalAlign = None,
        h_align: HorizontalAlign = None,
        parent: QtCore.QObject = None,
        spacing: int = None,
        geometry: Tuple[int, int, int, int] = None,
    ):
        """
        Layout

        Wrapper around QVBoxLayout and QHBoxLayout

        Parameters
        ----------

        widgets: List[QtWidgets.QWidget] = []
              List of widgets

        direction: Direction = Direction.Vertical
              Either a QHBoxLayout or QVBoxLayout

        v_align: VerticalAlign = None
              Vertical Alignment for Layout

        h_align: HorizontalAlign = None
              Horizontal Alignment for Layout

        parent: QtCore.QObject = None
              Parent widget

        spacing: int = None
              Spacing between widgets, default inherits from parent

        geometry: Tuple[int, int, int, int] = None
              Position of Widget
        """
        super(Layout, self).__init__(parent)
        self.layout: Union[
            QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout
        ] = direction.value()
        if v_align and h_align:
            self.layout.setAlignment(h_align.value | v_align.value)
        elif h_align:
            self.layout.setAlignment(h_align.value)
        elif v_align:
            self.layout.setAlignment(v_align.value)
        # self.layout.setAlignment(h_align.value)
        for widget in widgets:
            widget.set_parent(self)
            self.layout.addWidget(widget)
        if spacing:
            self.layout.setSpacing(spacing)
        if geometry:
            self.layout.setGeometry(QtCore.QRect(*geometry))
        self.setLayout(self.layout)
