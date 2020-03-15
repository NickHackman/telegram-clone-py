from __future__ import annotations

from pathlib import Path
import asyncio
import re
import json

from typing import (
    Callable,
    Dict,
    Any,
    Union,
    Pattern,
    List,
    Tuple,
    Final,
    Optional,
    Sequence,
)
from enum import Enum
from itertools import islice

from colorama import init  # type: ignore

from .config import Config, Mode
from .log import config_print, add_route_print, invalid_path_404, valid_path_200
from .header import construct_header


class Method(Enum):
    """
    HTTP Method that a Route can accept
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Type(Enum):
    """
    Valid Types for type coercision
    """

    Int = int
    Float = float
    Str = str

    @staticmethod
    def from_str(string: str) -> Tuple[Type, str]:
        """
        Converts a str representation of type to Type

        Parameters
        ----------

        string: str
             String to convert to type

        Returns
        -------

        Tuple[Type, str]

        Type: Type dictated by String
        str: Regex pattern for Type
        """
        if string == "int":
            return (Type.Int, r"/(\d+)")
        elif string == "float":
            return (Type.Float, r"/([\d\.]+)")
        return (Type.Str, r"/([^\/]+)")


class Rest:
    """
    A Flask-esque implementation
    """

    _routes: List[
        Tuple[Pattern[str], Method, List[Type], Callable[..., Dict[Any, Any]]]
    ]
    _config: Config

    def __init__(self, config_path: Union[str, Path]):
        self._routes = []
        self._config = Config.load_from_file(config_path)
        if self._config.mode is Mode.Debug:
            init(autoreset=True)
            config_print(self._config)

    def route(self, route_str: str, method: Method) -> Callable[..., Dict[Any, Any]]:
        """
        Route decorator calls function based on the provided Route and Method

        Decorated Function MUST return a value that is JSON serializable

        Parameters
        ----------

        route_str: str
             String that corresponds with this route

        Returns
        -------

        Callable[[str, Method], Any]
             Function that takes a route_str and a type and returns a dict that's JSON serializable

        Examples
        --------

        rest: Rest = Rest()

        # NOTE: if the type is KNOWN then provide it via <$TYPE:id>
        # Where $TYPE is in ["int", "float", "str"]
        @rest.route("/main/<str:name>/<int:age>", Method.GET)
        def hello_world(name: str, age: int) -> str:
            print(f"Hello {name}! You're {age - 1}")
        """

        def decorator(fun: Callable[..., Any]) -> Any:
            (ROUTE_PATTERN, types) = self._parse_route(route_str)
            self._routes.append((ROUTE_PATTERN, method, types, fun))
            if self._config.mode is Mode.Debug:
                add_route_print(route_str, fun)
            return fun

        return decorator

    @staticmethod
    def _parse_route(route_str: str) -> Tuple[Pattern[str], List[Type]]:
        """
        Parses the Route str constructing a Regex Pattern

        Parameters
        ----------

        route_str: str
             Route String that optionally has positional arguments

        Returns
        -------

        Pattern[str]
             Pattern that allows for positional arguments
        """
        types: List[Type] = []
        if route_str == "/":
            return (re.compile(r"^/$"), [])
        segments: List[str] = route_str.split("/")
        regex: str = r"^"
        for segment in islice(segments, 1, None):
            if segment.startswith("<") and segment.endswith(">"):
                if split := segment.split(":"):
                    (arg_type, pattern) = Type.from_str(split[0][1:])
                    types.append(arg_type)
                    regex += pattern
                else:
                    types.append(Type.Str)
                    regex += r"/([^\/]+)"
            else:
                regex += f"/{segment}"
        regex += r"$"
        return (re.compile(regex), types)

    def run(self) -> None:
        """
        Runs Asyncio event loop to recieve and process HTTP requests
        """

        async def handle_request(
            reader: asyncio.StreamReader, writer: asyncio.StreamWriter
        ) -> None:
            # TODO: 8192 is a decent constant value (used by most browsers as the max request size), but isn't perfect
            byte_msg = await reader.read(8192)
            msg = byte_msg.decode()
            (ip_address, _) = writer.get_extra_info("peername")
            output = self._serve(msg, ip_address)
            writer.write(output.encode())
            await writer.drain()
            writer.close()

        event_loop = asyncio.get_event_loop()
        server = asyncio.start_server(
            handle_request, self._config.host, self._config.port, loop=event_loop,
        )
        event_loop.run_until_complete(server)
        event_loop.run_forever()
        server.close()

    def _serve(self, request: str, ip_address: str) -> str:
        """
        Serves the HTTP Request a matching Route or a 404

        Parameters
        ----------

        request: str
              HTTP Request

        Returns
        -------

        an HTTP Response with the route's response or 404

        Exceptions
        ----------

        ValueError
             Coercision of argument failed
        """
        (path, req_method, payload) = self._parse_request(request)
        for (pattern, method, arg_types, route) in self._routes:
            if req_method == method and (match := pattern.match(path)):
                arguments: List[Any] = self._convert_arg_types(
                    match.groups(), arg_types
                )
                if self._config.mode is Mode.Debug:
                    valid_path_200(path, ip_address, req_method.value)
                if req_method in (Method.PUT, Method.POST):
                    return construct_header(200, "OK", route(*arguments, payload))
                return construct_header(200, "OK", route(*arguments))

        if self._config.mode is Mode.Debug:
            invalid_path_404(path, ip_address, req_method.value)
        return construct_header(404, "Not found")

    @staticmethod
    def _convert_arg_types(groups: Sequence[str], arg_types: List[Type]) -> List[Any]:
        """
        Coerces provided arguments to the provided types <int:age>

        Parameters
        ----------

        groups: Sequence[str]
             Values provided from URL

        arg_types: List[Type]
             Types corresponding to positional arguments

        Returns
        -------

        List[Any]
             Coerced positional arguments

        Exceptions
        ----------

        ValueError
             Provided argument can't be coerced into expected type
        """
        arguments: List[Any] = []
        for (item, arg_type) in zip(groups, arg_types):
            arguments.append(arg_type.value(item))
        return arguments

    @staticmethod
    def _parse_request(request: str) -> Tuple[str, Method, Optional[Dict[Any, Any]]]:
        """
        Parses request into important fields

        Parameters
        ----------

        request: str
             HTTP Request

        Returns
        -------

        Tuple[str, Method, Optional[str]]

        str: URL extension
        Method: HTTP Method
        Optional[str]: Optional Payload
        """
        first_line: List[str] = request.split("\r\n", 1)[0].split()
        method: Method = Method(first_line[0])
        if method is not Method.POST and method is not Method.PUT:
            return (first_line[1], method, None)
        split_msg: List[str] = request.split("\r\n\r\n")
        payload: Dict[Any, Any] = json.loads(split_msg[1])
        return (first_line[1], method, payload)
