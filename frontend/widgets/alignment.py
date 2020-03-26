"""
Alignment
"""
from enum import Enum

from PyQt5 import QtCore  # type: ignore


class HorizontalAlign(Enum):
    """
    Horizontal Alignment
    """

    Left = QtCore.Qt.AlignLeft
    Right = QtCore.Qt.AlignRight
    Center = QtCore.Qt.AlignHCenter
    Justify = QtCore.Qt.AlignJustify


class VerticalAlign(Enum):
    """
    Vertical Alignment
    """

    Bottom = QtCore.Qt.AlignBottom
    Center = QtCore.Qt.AlignVCenter
    Top = QtCore.Qt.AlignTop
    BaseLine = QtCore.Qt.AlignBaseline
