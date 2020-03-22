"""
Functions related to constructing HTTP headers
"""
from typing import Final, Dict, Any

import json
import textwrap
from datetime import datetime

CR: Final[str] = "\r"


def construct_header(code: int, phrase: str, payload: Dict[Any, Any] = {}) -> str:
    """
    Constructs HTTP Header and Payload

    Parameters
    ----------

    code: int
         HTTP Response code

    payload: str = ""
         Payload to send
    """
    return textwrap.dedent(
        f"""\
    HTTP/1.1 {code}{CR}
    server: il-legitimate-ferret-shaped-server{CR}
    date: {current_date()}{CR}
    content-type: application/json{CR}
    {CR}
    {json.dumps(payload)}
    """
    )


def current_date() -> str:
    """
    Get the current date

    Returns
    -------

    str
         properly formatted date
    """
    now = datetime.now()
    return now.strftime("%a, %d %b %Y %H:%M:%S %Z")
