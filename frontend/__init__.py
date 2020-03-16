#!/usr/bin/env python3
from components.chat_list import ChatList
from PyQt5.QtWidgets import QApplication

app = QApplication([])
header = ChatList()
header.show()
app.exec_()
