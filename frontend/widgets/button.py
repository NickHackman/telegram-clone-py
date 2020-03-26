"""
Button

Wrapper around QPushButton

functions
---------

button_icon
      Create QIcon

Classes
-------

Button
       Wrapper around QPushButton
"""
from typing import Callable, Tuple, Union

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .qtwidget import QtWidget


def button_icon(icon_path: str) -> QtGui.QIcon:
    """
    Creates a QIcon from an icon_path

    Parameters
    ----------

    icon_path: str
           Path to icon

    Returns
    -------

    QtGui.QIcon
          Qt Icon for Button
    """
    return QtGui.QIcon(QtGui.QPixmap(icon_path))


class Button(QtWidget):
    """
    Wrapper around QPushButton

    Parameters
    ----------

    inner: Union[QtGui.QIcon, str]
         Either an QIcon or String for the Button's inner widget

    flat: bool = False
          Whether the button is flat or not

    on_click: Callable[..., None] = None
          On Click callback function

    enabled: bool = True
          Whether or not the Button is enabled

    geometry: Tuple[int, int, int, int] = None
          Location of for Button

    parent: QtWidgets.QWidget = None
          Parent widget
    """

    button: QtWidgets.QPushButton

    def __init__(
        self,
        inner: Union[QtGui.QIcon, str],
        *,
        flat: bool = False,
        on_click: Callable[..., None] = None,
        enabled: bool = True,
        geometry: Tuple[int, int, int, int] = None,
        parent: QtWidgets.QWidget = None,
    ):
        super(Button, self).__init__(parent)
        if isinstance(inner, QtGui.QIcon):
            self.button = QtWidgets.QPushButton(inner, "", self)
        else:
            self.button = QtWidgets.QPushButton(inner, self)
        self.button.setFlat(flat)
        if geometry:
            self.button.setGeometry(QtCore.QRect(*geometry))
        if on_click:
            self.button.clicked.connect(on_click)
        self.button.setEnabled(enabled)
        self.button.setIconSize(QtCore.QSize(100, 100))
