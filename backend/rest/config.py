"""
Contains Config dataclass and Modes for Rest Server
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Final
from pathlib import Path
from enum import Enum
import json


class Mode(Enum):
    """
    Available Modes to run Rest

    Debug
    -----
    Prints and logs information about routes being executed

    Production
    ----------
    Logs executed routes to log_file
    """

    Debug = "debug"
    Production = "production"


@dataclass
class Config:
    """
    Config dataclass that stores all data specific to running the Rest Server
    """

    host: str
    port: int
    log_file: str
    secret: str
    mode: Mode = Mode.Debug

    def __init__(
        self, host: str, port: int, log_file: str, mode: str, secret: str,
    ):
        """
        Constructs a Config

        Parameters
        ----------

        host: str
             Host portion of URL to host on
        port: int
             Port number to host on
        log_file: str
             Location of log file
        mode: str
             Mode either debug or production
        secret: str
             Secret code
        websocket_port: int
             Port for websocket must be different than port

        """
        self.host = host
        self.port = port
        self.log_file = log_file
        self.mode = Mode(mode)
        self.secret = secret

    @staticmethod
    def load_from_file(path: Union[Path, str]) -> Config:
        """
        Loads JSON config file from path

        Parameters
        ----------

        path: Union[Path, str]
             Path to config file

        Returns
        -------

        Config
             Config instance loaded from path
        """
        PATH: Final[Path] = Path(path)
        if not PATH.exists() or PATH.is_dir():
            raise IOError(f"{path} doesn't exist or is a directory")
        with open(PATH, "r") as file:
            config_json = json.load(file)
            return Config(**config_json)
