from typing import Callable, Tuple

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class ImageButton(QWidget):
    _button: QPushButton

    def __init__(
        self,
        icon: str,
        callback: Callable,
        text: str = "",
        *,
        size: Tuple[int, int] = (24, 24)
    ):
        """
        A Qt5 Image Button

        Remember to call ImageButton.show()

        Parameters
        ----------

        icon: str
             Path to image

        callback: Callable
             Function to execute when button is pushed

        text: str = ""
             [Optional] message to put with icon

        size: Tuple[int, int] = (24, 24)
             Size of the Icon in the Button
        """
        QWidget.__init__(self)
        self._button = QPushButton(text, self)
        self._button.clicked.connect(callback)
        self._button.setIcon(QIcon(icon))
        self._button.setIconSize(QSize(*size))
        layout = QVBoxLayout(self)
        layout.addWidget(self._button)
