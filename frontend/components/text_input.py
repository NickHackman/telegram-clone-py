#!/usr/bin/env python3
from typing import Callable, Optional

from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout  # type: ignore
from PyQt5.QtCore import QRegExp  # type: ignore
from PyQt5.QtGui import QRegExpValidator  # type: ignore


class TextInput(QWidget):
    _text_input: QLineEdit
    text_changed: Optional[Callable[[str], None]]

    def __init__(
        self,
        *,
        hint: str = "",
        text_changed: Optional[Callable[[str], None]] = None,
        validator: Optional[str] = None,
        width: int = 64,
        height: int = 32
    ):
        """
        Constructs a standard TextInput

        Parameters
        ----------

        hint: str = ""
             Placeholder text

        text_changed: Callable[[str], None]
             Function to be called when text changes

        validator: Optional[str] = None
             Validator regular expression

        width: int = 64
             Default width of TextInput

        height: int = 32
             Default height of TextInput
        """
        QWidget.__init__(self)
        layout = QHBoxLayout(self)
        self._text_input = QLineEdit()
        self._text_input.setPlaceholderText(hint)
        self.text_changed = text_changed
        self._text_input.textChanged.connect(self._text_changed)
        if validator is not None:
            self._text_input.setValidator(
                QRegExpValidator(QRegExp(validator), self._text_input)
            )
        layout.addWidget(self._text_input)

    @property
    def text(self) -> str:
        """
        Get Text in input

        Returns
        -------

        str
             String in QLineEdit
        """
        return self._text_input.text()

    def _text_changed(self, text: str) -> None:
        """
        Calls provided textChanged function and stores the text

        Parameters
        ----------

        text: str
             Text currently in the QLineEdit
        """
        if self.text_changed:
            self.text_changed(text)
