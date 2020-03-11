#!/usr/bin/env python3
"""
Request-esque HTTP Request library

Main entry point is request, but like Requests has get, post, put, and delete.
Doesn't have any extra HTTP Requests that won't be used by this application
"""

from .response import Response
from .client import Client
from .header import Method


def request(url: str, method: Method, *, data: str = "") -> Response:
    """
    Main Request entry point

    allows for any type of request for a URL

    Parameters
    ----------

    url: str
         URL to send the HTTP Request to, must be in the form of https://domain.com/file/path

    method: Method
         Type of HTTP Method to use GET, PUT, POST and DELETE

    Returns
    -------

    Response
          Returns Response from Server, this should be checked to see if it's an error with either
             Response.raise_for_status() or an if check of Response.is_error()
    """
    client: Client = Client(url, method)
    payload: bytes = client.construct_payload(data)
    client.send(payload)
    response: Response = client.recieve()
    return response


def get(url: str) -> Response:
    """
    GET Request

    allows for any type of request for a URL

    Parameters
    ----------

    url: str
         URL to send the HTTP Request to, must be in the form of https://domain.com/file/path

    Returns
    -------

    Response
          Returns Response from Server, this should be checked to see if it's an error with either
             Response.raise_for_status() or an if check of Response.is_error()
    """
    return request(url, Method.GET)


def post(url: str, payload: str) -> Response:
    """
    POST Request

    allows for any type of request for a URL

    Parameters
    ----------

    url: str
         URL to send the HTTP Request to, must be in the form of https://domain.com/file/path

    payload: str
         Data to be put into HTTP Request

    Returns
    -------

    Response
          Returns Response from Server, this should be checked to see if it's an error with either
             Response.raise_for_status() or an if check of Response.is_error()
    """
    return request(url, Method.POST, data=payload)


def put(url: str) -> Response:
    """
    PUT Request

    allows for any type of request for a URL

    Parameters
    ----------

    url: str
         URL to send the HTTP Request to, must be in the form of https://domain.com/file/path

    Returns
    -------

    Response
          Returns Response from Server, this should be checked to see if it's an error with either
             Response.raise_for_status() or an if check of Response.is_error()
    """
    return request(url, Method.PUT)


def delete(url: str) -> Response:
    """
    DELETE Request

    allows for any type of request for a URL

    Parameters
    ----------

    url: str
         URL to send the HTTP Request to, must be in the form of https://domain.com/file/path

    Returns
    -------

    Response
          Returns Response from Server, this should be checked to see if it's an error with either
             Response.raise_for_status() or an if check of Response.is_error()
    """
    return request(url, Method.DELETE)
