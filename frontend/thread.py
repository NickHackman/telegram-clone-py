from typing import Any, List, Callable, Tuple

from PyQt5 import QtCore  # type: ignore


class QtThread(QtCore.QThread):
    args: Tuple[Any, ...]

    def __init__(self, fun, finished: QtCore.pyqtSignal, *args):
        super(QtThread, self).__init__(None)
        self.fun = fun
        self._finished = finished
        self.args = args

    def run(self) -> None:
        result: Any = self.fun(*self.args)
        self._finished.emit(result)

    def __del__(self):
        self.wait()
