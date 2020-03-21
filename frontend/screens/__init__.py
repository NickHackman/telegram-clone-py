"""
Contains all Screens for the Telegram-clone-py Frontend

The __init__.py file contains a Router in order to navigate between screens more easily
Also contains all Assets paths
"""
import os
from pathlib import Path
from typing import Dict, Callable, Any, List, Tuple

from PyQt5 import QtWidgets  # type: ignore

# Assets (absolute) paths
ASSETS: str = f"{Path(__file__).parent.parent.absolute()}{os.sep}assets"

TELEGRAM_ICON: str = f"{ASSETS}{os.sep}telegram-clone-py-icon.svg"
EMOTICON_ICON: str = f"{ASSETS}{os.sep}emoticon.svg"
MENU_ICON: str = f"{ASSETS}{os.sep}menu.svg"
SEARCH_ICON: str = f"{ASSETS}{os.sep}search.svg"
SEND_ICON: str = f"{ASSETS}{os.sep}send.svg"
BACKARROW_ICON: str = f"{ASSETS}{os.sep}back-arrow.svg"


class InvalidRouteError(Exception):
    """Route called that doesn't exist in self.routes"""


class Router:
    """
    An emulation of React-Router that also maintains State

    Attributes
    ----------

    state: Dict[str, Any]
         Stores State variables for application (Not Thread safe),
         but that doesn't matter. State is only going to store URL,
         Port and User JWT

    route_stack: List[Tuple[str, Callable[..., Any], List[Any]]]
         The stack that stores the function name, function and a list of parameters
         that were used to call it, so that it can be walked backwards

    routes: Dict[str, Any]
         A Dictionary of the name of the route and the Class init that it calls
    """

    state: Dict[str, Any]
    route_stack: List[Tuple[str, Callable[..., Any], QtWidgets.QMainWindow]]
    routes: Dict[str, Any]

    def __init__(
        self,
        routes: Dict[str, Any],
        setup_route_fun: Callable[..., None],
        first_route: Tuple[str, Callable[..., Any], QtWidgets.QMainWindow],
    ):
        """
        Constructs a Router instance

        Parameters
        ----------

        routes: Dict[str, Any]
             Valid routes by name and their corresponding Function calls

        setup_route_fun: Callable[..., None]
             Function that setups up the Route to be executed

        first_route: Tuple[str, Callable[..., Any], QtWidgets.QMainWindow]
             As a result Qt requiring the event loop to be started
             immediately after showing the first window, the first route must be
             executed manually and not through Router, but must still exist on the
             route_stack
        """
        self.state: Dict[str, Any] = {}
        self.route_stack: List[
            Tuple[str, Callable[..., Any], QtWidgets.QMainWindow]
        ] = [first_route]
        self.routes: Dict[str, Any] = routes
        self.setup_route_fun: Callable[..., None] = setup_route_fun

    def push(self, route_name: str, window: QtWidgets.QMainWindow) -> None:
        """
        Pushes a Route onto the stack

        Parameters
        ----------

        route_name: str
             Route to push on

        window: QMainWindow
             Qt main window to pass around

        Exceptions
        ----------

        InvalidRouteError
             If the route doesn't exist in self.routes
        """
        try:
            self.route_stack.append((route_name, self.routes[route_name], window))
            # Pass in arguments and Router
            self.setup_route_fun(window, self.routes[route_name](self))
        except KeyError:
            raise InvalidRouteError(
                f"Route: {route_name} does not exist in {self.routes}"
            )

    def pop(self) -> None:
        """
        Pops one Route off the stack executing it

        Exceptions
        ----------

        If already on the top of the stack, does NOTHING
        """
        try:
            # Pop current window off
            self.route_stack.pop()
            (_, fun, window) = self.route_stack[-1]
            self.setup_route_fun(window, fun(self))
        except IndexError:
            pass

    def pop_until(self, until_name: str) -> None:
        """
        Pops routes off until it reaches the provided route name, executing that route

        Parameters
        ----------

        until_name: str
              Route name to pop until

        Exceptions
        ----------

        It will pop off all routes until it reaches the top
           of the stack and then do NOTHING
        """
        try:
            while route := self.route_stack.pop():
                (name, fun, window) = route
                if until_name == name:
                    self.setup_route_fun(window, fun(self))
                    break
        except IndexError:
            pass

    def set_state(self, name: str, value: Any) -> None:
        """
        Adds a Key, Value pair to the State

        Parameters
        ----------

        name: str
            Name to store as

        value: Any
            Value to store
        """
        self.state[name] = value

    def rm_state(self, name: str) -> Any:
        """
        Removes a value from the State returning it

        Parameter
        ---------

        name: str
             Name to remove

        Returns
        -------

        Any
             Value stored with corresponding name
        """
        try:
            value: Any = self.state[name]
            del self.state[name]
            return value
        except KeyError:
            pass

    def clear_state(self) -> Dict[str, Any]:
        """
        Clears the state, returning the previous state

        Returns
        -------

        Dict[str, Any]
             Previous state
        """
        prev_state: Dict[str, Any] = self.state
        self.state = {}
        return prev_state

    def add_route(self, route_name: str, route: Callable[..., Any]) -> None:
        """
        Adds a route to Router's routes
        """
        self.routes[route_name] = route
