#!/usr/bin/env python3
from enum import Enum
import ssl
import time
import socket
from urllib.parse import urlparse, ParseResult
from typing import List

from .response import Response, HTTPError
from .response_parser import ResponseParser
from .header import Header, Method


class Scheme(Enum):
    http = 80
    https = 443


class Client:
    _scheme: Scheme
    _socket: socket.socket
    _method: Method
    _parsed_url: ParseResult

    def __init__(self, url: str, method: Method):
        """
        Constructs a Client

        Parameters
        ----------

        url: str
             URL for the end host to send the request to

        method: Method
             HTTP method to use GET, PUT, DELETE or POST
        """
        self._parsed_url = urlparse(url)
        self._scheme = Scheme[self._parsed_url.scheme]
        self._method = method

    @staticmethod
    def _setup_ssl() -> ssl.SSLContext:
        """
        Establishes the SSL encrypted connection

        uses TLSv1_2 and requires Certs

        Returns
        -------

        ssl.SSLContext
             The established context for the HTTPs connection
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        return context

    def construct_payload(
        self,
        payload: str = "",
        *,
        accept: str = "application/json",
        http_version: str = "HTTP/1.1",
        user_agent: str = "Requests",
    ) -> bytes:
        """
        Constructs the request by creating a header and attaching the payload

        Result should be passed into Client.send()

        Parameters
        ----------

        payload: str = ""
             Body of Request

        accept: str = "application/json"
             Response type to accept

        http_version: str = "HTTP/1.1"
             Version of HTTP to use

        user_agent: str = "Requests"
             User agent to display to websites
        """
        extension = self._parsed_url.path
        if self._parsed_url.query:
            extension += f"?{self._parsed_url.query}"

        header: Header = Header(
            self._parsed_url.netloc,
            # If no extension assume /
            extension or "/",
            self._method,
            accept=accept,
            http_version=http_version,
            user_agent=user_agent,
        )
        header_bytes: bytes = header.to_bytes()
        return header_bytes + "\r\n\r\n".encode() + payload.encode("utf-8")

    def send(self, payload: bytes) -> None:
        """
        Send the HTTP or HTTPs request

        Parameters
        ----------

        payload: bytes
             Combination of Header and Payload to send
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._scheme is Scheme.https:
                context: ssl.SSLContext = self._setup_ssl()
                self._socket = context.wrap_socket(
                    self._socket, server_hostname=self._parsed_url.netloc
                )

            if (possible_port := self._parsed_url.netloc.split(":")) is not None:
                self._socket.connect((possible_port[0], int(possible_port[1])))
            else:
                self._socket.connect((self._parsed_url.netloc, self._scheme.value))
            self._socket.send(payload)
        except Exception as e:
            raise HTTPError(str(e), None)

    def recieve(self, timeout: int = 1) -> Response:
        """
        Recieves the HTTP Response from Server

        Closes the socket in use

        Returns
        -------

        Response
             The Response from the Server
        """
        self._socket.setblocking(False)
        data: List[bytes] = []
        begin = time.time()

        while True:
            # Data recieved
            if data and time.time() - begin > timeout:
                break
            # Timeout reached
            elif time.time() - begin > timeout * 2:
                break
            try:
                if recieved := self._socket.recv(8192):
                    data.append(recieved)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except socket.error:
                pass
        result = (b"".join(data)).decode()
        self._socket.close()
        parser = ResponseParser(result)
        return parser.parse()
