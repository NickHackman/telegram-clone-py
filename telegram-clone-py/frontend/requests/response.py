from dataclasses import dataclass
from typing import Dict, Any

from .status_code import StatusCode


@dataclass
class Response:
    """
    HTTP Response with headers, status_code, and payload

    Parameters
    ----------

    status_code: StatusCode
         HTTP status code and phrase

    http_version: str
         Version of HTTP

    header: Dict[str, str]
         Header of the HTTP Response

    json: Dict[Any, Any]
         Parsed JSON in HTTP Response
    """

    status_code: StatusCode
    http_version: str
    header: Dict[str, str]
    json: Dict[Any, Any]

    def raise_for_status(self) -> None:
        """
        Raises an Exception if an HTTPError occurred

        Exceptions
        ----------

        HTTPError
             With a message describing the error and self
        """
        if self.status_code.is_client_error():
            raise HTTPError(f"Client Error: {self.status_code}", self)
        elif self.status_code.is_server_error():
            raise HTTPError(f"Server Error: {self.status_code}", self)

    def is_error(self) -> bool:
        """
        Check if a response is an HTTPError

        Returns
        -------

        bool
             whether or not an HTTPError occurred
        """
        return self.status_code.is_error()


class HTTPError(Exception):
    """
    HTTPError occurred meaning Code wasn't a 2xx value
    """

    response: Response

    def __init__(self, message: str, response: Response):
        """
        Constructs an HTTPError

        Parameters
        ----------

        message: str
             Exception message

        response: Response
             Corresponding Response
        """
        self.response = response
        super().__init__(message)
