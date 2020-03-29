"""
Alignment
"""
from enum import Enum
from typing import Pattern, Callable, Tuple, Final

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore


class Align(Enum):
    """
    Alignment
    """

    Left = QtCore.Qt.AlignLeft
    Right = QtCore.Qt.AlignRight
    Center = QtCore.Qt.AlignCenter
    Justify = QtCore.Qt.AlignJustify
