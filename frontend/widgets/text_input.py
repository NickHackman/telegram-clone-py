"""
Input

A Wrapper around QLineEdit to reduce verbosity

Enums
-----

Echo
      How to display text

Classes
-------

Input
      Wrapper around QLineEdit

Constants
---------

STYLESHEET
       Stylesheet to apply to QLineEdit
"""
from enum import Enum
from typing import Pattern, Callable, Tuple, Final

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .alignment import Align


class Echo(Enum):
    """
    Echo Method

    Variants
    --------

    Normal
         Display text

    Password
         Replace text with asteriks

    NoEcho
         Display nothing

    PasswordEchoOnEdit
         Display until input is left and then display aterisk instead
    """

    Normal = QtWidgets.QLineEdit.Normal
    Password = QtWidgets.QLineEdit.Password
    NoEcho = QtWidgets.QLineEdit.NoEcho
    PasswordEchoOnEdit = QtWidgets.QLineEdit.PasswordEchoOnEdit


STYLESHEET: Final[
    str
] = """\
color: rgb(255, 255, 255);
background-color: rgb(36, 47, 61);
border-radius: 2px;
"""


class TextInput(QtWidgets.QWidget):
    """
    Constructs an Input

    A usability Wrapper around QLineEdit

    Parameters
    ----------

    placeholder: str
         Placeholder text

    max_length: int = 144
         Max length of input

    validator: Pattern[str] = None
         Regular Expression to apply to Input

    parent: QtCore.QObject = None
         Parent Qt Object

    echo: Echo = Echo.Normal
         Echo type, how to display typed text

    align: Align = Align.Left
         Alignment for text

    editing_finished: Callable[None, None] = None
         Callback when finished editing

    text_changed: Callable[[str], None] = None
         Callback when text changes

    font: Tuple[str, int] = ("Arial", 12)
         Font for text

    read_only: bool = False
         Whether or not the Input is read only

    clear_button: bool = False
         Display clear button in Input

    min_size: Tuple[int, int] = None
         Minimum Size, if None let Qt decide
    """

    line_edit: QtWidgets.QLineEdit

    def __init__(
        self,
        placeholder: str,
        *,
        max_length: int = 144,
        validator: Pattern[str] = None,
        parent: QtCore.QObject = None,
        echo: Echo = Echo.Normal,
        align: Align = Align.Left,
        editing_finished: Callable[..., None] = None,
        text_changed: Callable[[str], None] = None,
        font: Tuple[str, int] = ("Arial", 12),
        read_only: bool = False,
        clear_button: bool = False,
        min_size: Tuple[int, int] = None,
    ):
        super(TextInput, self).__init__(parent)
        self.line_edit = QtWidgets.QLineEdit(placeholder, self)
        self.line_edit.setMaxLength(max_length)
        self.line_edit.setEchoMode(echo.value)
        if validator:
            self.line_edit.setValidator(QtGui.QRegExpValidator(validator))
        self.line_edit.setAlignment(align.value)
        if text_changed:
            self.line_edit.textChanged(text_changed)
        if editing_finished:
            self.line_edit.editingFinished(editing_finished)
        self.line_edit.setFont(*font)
        self.line_edit.setReadOnly(read_only)
        self.line_edit.setStyleSheet(STYLESHEET)
        self.line_edit.setClearButtonEnabled(clear_button)
        if min_size:
            self.line_edit.setMinimumSize(*min_size)

    @property
    def text(self) -> str:
        """
        Get text

        Returns
        -------

        str
              Text stored in interior QLineEdit
        """
        return self.line_edit.text()
