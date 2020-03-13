#!/usr/bin/env python3
from typing import Callable

from colorama import Fore, Style  # type: ignore

from .config import Config


def add_route_print(path: str, fun: Callable) -> None:
    """
    Prints every loaded Route to the console

    Parameters
    ----------

    path: str
         URL for the route

    fun: Callable
         Function the route calls
    """
    print(f"➕ {Style.BRIGHT + 'route'}: '{path}' -> {fun.__name__}")


def config_print(config: Config) -> None:
    """
    Prints the loaded Configuration file to the console

    Parameters
    ----------

    config: Config
         Currently loaded configuration file
    """
    print(f"{Fore.GREEN + Style.BRIGHT + 'Rest'} starting...")
    print(f"{Style.BRIGHT + 'Log file'}: {config.log_file}")
    url: str = f"http://{config.host}:{config.port}"
    print(f"{Style.BRIGHT + 'Localhost URL'}: {Fore.BLUE + url}")
    print(f"{Style.BRIGHT + 'Mode'}: {Style.BRIGHT + Fore.YELLOW + 'debug'}")
    print("Press CTRL + C to quit\n")


def invalid_path_404(path: str, ip_address: str) -> None:
    """
    Prints 404 for URL and IP address

    Parameters
    ----------

    path: str
         url that isn't valid

    ip_address: str
         IP address that attempted to access that url
    """
    print(
        f"❌ {Fore.RED + Style.BRIGHT + '404'} {Style.BRIGHT + path} from {ip_address}"
    )


def valid_path_200(path: str, ip_address: str) -> None:
    """
    Prints 200 for URL and IP address

    Parameters
    ----------

    path: str
         url that is valid

    ip_address: str
         IP address that attempted to access that url
    """
    print(
        f"✔ {Fore.GREEN + Style.BRIGHT + '200'} {Style.BRIGHT + path} from {ip_address}"
    )
