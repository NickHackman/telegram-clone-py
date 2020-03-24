"""
Form related functionality

Classes
-------

FormEntry
     An Entry in a Form

Form
     A QFormLayout wrapper
"""
from typing import List, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

from .text import Text
from .text_input import TextInput
from .alignment import Align


class FormEntry:
    """
    FormEntry

    Parameters
    ----------

    label: Text
         Label part of form

    text_input: TextInput
         Input part of form
    """

    label: Text
    text_input: TextInput

    def __init__(self, *, label: Text, text_input: TextInput):
        self.label = label
        self.text_input


class Form(QtWidgets.QWidget):
    """
    Form

    Parameters
    ----------

    labeled_inputs: List[FormEntry] = []
         List of FormEntries with their labels and inputs

    geometry: Tuple[int, int, int, int] = None
         Geometry

    align: Align = Align.Left
         Alignment of rows

    horizontal_spacing: int = None
         Set Horizontal spacing, defaults to inherit from parent

    vertical_spacing: int = None
         Set Vertical spacing, defaults to inherit from parent

    parent: QtCore.QObject = None
         Parent Widget
    """

    def __init__(
        self,
        *,
        labeled_inputs: List[FormEntry] = [],
        geometry: Tuple[int, int, int, int] = None,
        align: Align = Align.Left,
        horizontal_spacing: int = None,
        vertical_spacing: int = None,
        parent: QtCore.QObject = None
    ):
        super(Form, self).__init__(parent)
        form_layout = QtWidgets.QFormLayout(self)
        for index, entry in enumerate(labeled_inputs):
            form_layout.setWidget(index, QtWidgets.QFormLayout.LabelRole, entry.label)
            form_layout.setWidget(
                index, QtWidgets.QFormLayout.FieldRole, entry.text_input
            )
        if geometry:
            form_layout.setGeometry(*geometry)
        if horizontal_spacing:
            form_layout.setHorizontalSpacing(horizontal_spacing)
        if vertical_spacing:
            form_layout.setVerticalSpacing(vertical_spacing)
        form_layout.setAlignment(align.value)
        self.setLayout(form_layout)
