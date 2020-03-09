#!/usr/bin/env python3
from typing import Dict, Any

from .status_code import StatusCode


class Response:
    status_code: StatusCode
    http_version: str

    def __init__(self, response: str):
        pass

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

    def json(self) -> Dict[Any, Any]:
        pass


class HTTPError(Exception):
    response: Response

    def __init__(self, message: str, response: Response):
        self.response = response
        super().__init__(message)
