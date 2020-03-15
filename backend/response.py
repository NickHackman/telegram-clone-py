#!/usr/bin/env python3

from typing import Any, Dict

from enum import Enum


class Status(Enum):
    """
    Status for Response
    """

    Success = "success"
    Failure = "failure"
    Error = "error"


def response(status: Status, response: Any) -> Dict[str, Any]:
    return {"status": status.value, "response": response}
