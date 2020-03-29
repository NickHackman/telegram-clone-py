import sys

from typing import Any, Dict, Tuple, Callable

from PyQt5.QtWidgets import QApplication, QMainWindow  # type: ignore

from .screens import Router
from .screens.login import Login
from .screens.create_account import CreateAccount
from .screens.connect_to_server import ConnectToServer
from .screens.main import Main


def setup_route_function(window: QMainWindow, screen_object: Any) -> None:
    """
    Faciliate switching Windows for Router

    Parameters
    ----------

    window: QMainWindow
         MainWindow of Qt Application

    screen_object: Any
         Screen Object that can setup a MainWindow
    """
    screen_object.setupUi(window)
    window.show()


routes: Dict[str, Any] = {
    "/": ConnectToServer,
    "/login": Login,
    "/create/account": CreateAccount,
    "/main": Main,
}

app = QApplication(sys.argv)
main_window = QMainWindow()
first_route: Tuple[str, Callable[..., Any], QMainWindow] = (
    "/",
    ConnectToServer,
    main_window,
)
router: Router = Router(routes, setup_route_function, first_route)
setup_route_function(main_window, ConnectToServer(router))
sys.exit(app.exec_())
