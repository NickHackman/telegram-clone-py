"""
Widgets that are wrappers around QtWidgets

Purporse
--------

Emulate Flutter declaritive Widgets, for ease of use and
  reduce verbosity than standard PyQt

Widgets
-------

Text
     QLabel Wrapper

Input
     QLineEdit Wrapper

Layout
     QVBoxLayout and QHBoxLayout wrapper

Icon
     QLabel that has a PixMap

Align
     Alignment for text widgets (Text and Input)

FormEntry
     A row in a QFormLayout

Form
     QFormLayout Wrapper

Button
     QPushButton Wrapper

Example
-------

from .text_input import TextInput
from .layout import Layout, Direction
from .form import Form, FormEntry
from .text import Text
from .button import Button

Layout(
    direction=Direction.Vertical,
    widgets=[
        Text("Connect to Server"),
        Form(
            labeled_inputs=[
                FormEntry(label=Text("url"), text_input=TextInput("Url")),
                FormEntry(
                    label=Text("Port"), text_input=TextInput("Port", validator=r"\d+")
                ),
            ]
        ),
        Button("Connect"),
    ],
)
"""

# Expose Public API
from .text_input import TextInput, Echo
from .layout import Layout, Direction
from .form import Form, FormEntry
from .text import Text
from .icon import Icon
from .button import Button, button_icon
from .alignment import Align
