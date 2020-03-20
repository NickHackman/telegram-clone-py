from itertools import islice
import json
import re
from typing import Dict, Any, List, Tuple

from .response import Response
from .status_code import StatusCode


class ResponseParser:
    """
    Parses an HTTP response into its corresponding fields
    """

    _response: str
    _line_number: int = 0

    def __init__(self, response: str):
        """
        Constructs a ResponseParser

        Parameters
        ----------

        response: str
             The response in UTF-8
        """
        self._response = response

    def _parse_header(self, lines: List[str]) -> Dict[str, str]:
        """
        Parses the Header section of the response

        Parameters
        ----------

        lines: List[str]
              Lines that are part of the header

        Returns
        -------

        Dict[str, str]
             The header as Key value pairs
        """
        HEADER_REGEX = re.compile(r"^(.+): (.+)$")
        header: Dict[str, str] = {}
        for line in islice(lines, self._line_number, None):
            self._line_number += 1
            if not line:
                break
            (key, value) = HEADER_REGEX.findall(line)[0]
            header[key] = value
        return header

    def _parse_first_line(self, line: str) -> Tuple[str, StatusCode]:
        """
        Parses the first line of the Response

        Parameters
        ----------

        line: str
             First line

        Returns
        -------

        (str, StatusCode)
             the Version and StatusCode
        """
        parts = line.split()
        code = StatusCode(int(parts[1]))
        self._line_number += 1
        return (parts[0], code)

    def _parse_json(self, lines: List[str]) -> Dict[Any, Any]:
        """
        Parses the payload in the response as JSON

        Parameters
        ----------

        lines: List[str]
             the remaining lines

        Returns
        -------

        Dict[Any, Any]
             The JSON parsed
        """
        string: str = ""
        for s in lines:
            string += s
        return json.loads(string)

    def parse(self) -> Response:
        """
        Parses Response into Response object

        Returns
        -------

        Response
             Response that contains the corresponding fields
        """
        lines: List[str] = self._response.splitlines()
        (version, code) = self._parse_first_line(lines[self._line_number])
        header: Dict[str, str] = self._parse_header(lines)
        try:
            json = self._parse_json(lines[self._line_number :])
            return Response(code, version, header, json)
        except Exception:
            return Response(code, version, header, {})
