from typing import Callable, Optional
from enum import Enum

from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout  # type: ignore
from PyQt5.QtCore import QRegExp  # type: ignore
from PyQt5.QtGui import QRegExpValidator  # type: ignore


class InputType(Enum):
    """
    Input Types

    Variants
    ------

    Password
        Display Asteriks rather than actual text

    Normal
        Display Text

    NoEcho
        Display Nothing

    PasswordEchoOnEdit
        Display only the most recently entered characters, but not previous
    """

    Password = QLineEdit.Password
    Normal = QLineEdit.Normal
    NoEcho = QLineEdit.NoEcho
    PasswordEchoOnEdit = QLineEdit.PasswordEchoOnEdit


class TextInput(QWidget):
    _text_input: QLineEdit
    text_changed: Optional[Callable[[str], None]]

    def __init__(
        self,
        *,
        hint: str = "",
        text_changed: Optional[Callable[[str], None]] = None,
        validator: Optional[str] = None,
        input_type: InputType = InputType.Normal,
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

        input_type: InputType = InputType.Normal
             How to display text

        width: int = 64
             Default width of TextInput

        height: int = 32
             Default height of TextInput
        """
        QWidget.__init__(self)
        layout = QHBoxLayout(self)
        self._text_input = QLineEdit()
        self._text_input.setPlaceholderText(hint)
        self._text_input.setEchoMode(input_type.value)
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
