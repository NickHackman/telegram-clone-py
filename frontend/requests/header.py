from typing import Final, Dict
from enum import Enum


class Method(Enum):
    """
    Type of HTTP Request

    Supported: GET, PUT, DELETE and POST
    """

    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    POST = "POST"


CLRF: Final[str] = "\r\n"


class Header:
    _dict: Dict[str, str]
    _method: Method
    _extension: str = "/"
    _host: str
    _protocol: str

    def __init__(
        self,
        host: str,
        extension: str = "/",
        method: Method = Method.GET,
        *,
        accept: str = "application/json",
        http_version: str = "HTTP/1.1",
        user_agent: str = "Requests",
    ):
        """
        Constructs Header

        Parameters
        ----------

        host: str
             Hostname of servre
        extension: str = "/"
             File extension, parameters, query as a str
        method: Method = Method.GET
             Type of HTTP method to use
        accept: str = "application/json"
             Acceptable response type
        http_version: str = "HTTP/1.1"
             Version of HTTP
        user_agent: str = "Requests"
             User agent to display to server
        """
        self._method = method
        self._host = host
        self._extension = extension
        self._protocol = http_version
        self._dict = {
            "User-Agent": user_agent,
            # "Accept": accept,
            "Accept-Language": "en-us",
            "Accept-Decoding": "gzip,deflate",
            "Accept-Charset": "ISO-8859-1,utf-8",
        }

    def to_bytes(self) -> bytes:
        """
        Encodes the Header into UTF-8 bytes

        Returns
        -------

        bytes
             UTF-8 byte stream
        """
        header_str: str = f"{self._method.value} {self._extension} {self._protocol}{CLRF}Host: {self._host}{CLRF}"
        for (key, value) in self._dict.items():
            header_str += f"{key}: {value}{CLRF}"
        return header_str.encode("utf-8")
