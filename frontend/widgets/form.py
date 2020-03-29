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

from PyQt5 import QtCore, QtWidgets  # type: ignore

from .alignment import HorizontalAlign, VerticalAlign
from .text import Text
from .text_input import TextInput
from .qtwidget import QtWidget


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
        self.text_input = text_input


class Form(QtWidget):
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
        v_align: VerticalAlign = VerticalAlign.Center,
        h_align: HorizontalAlign = HorizontalAlign.Center,
        horizontal_spacing: int = None,
        vertical_spacing: int = None,
        parent: QtCore.QObject = None
    ):
        super(Form, self).__init__(parent)
        self.form_layout = QtWidgets.QFormLayout(self)
        for index, entry in enumerate(labeled_inputs):
            entry.label.set_parent(self)
            self.form_layout.setWidget(
                index, QtWidgets.QFormLayout.LabelRole, entry.label
            )
            entry.text_input.set_parent(self)
            self.form_layout.setWidget(
                index, QtWidgets.QFormLayout.FieldRole, entry.text_input
            )
        if geometry:
            self.setGeometry(QtCore.QRect(*geometry))
        if horizontal_spacing:
            self.form_layout.setHorizontalSpacing(horizontal_spacing)
        if vertical_spacing:
            self.form_layout.setVerticalSpacing(vertical_spacing)
        self.form_layout.setAlignment(v_align.value | h_align.value)
        self.setLayout(self.form_layout)
