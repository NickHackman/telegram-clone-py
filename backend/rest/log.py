"""
Contains all printing and logging funcionality
"""
from typing import Callable

from colorama import Fore, Style  # type: ignore

from .config import Config


def add_route_print(path: str, method, fun: Callable) -> None:
    """
    Prints every loaded Route to the console

    Parameters
    ----------

    path: str
         URL for the route

    fun: Callable
         Function the route calls
    """
    method_print: str = ""
    if method.value == "DELETE":
        method_print = f"{Fore.RED}{method.value}{Fore.RESET}"
    elif method.value == "POST":
        method_print = f"{Fore.GREEN}{method.value}{Fore.RESET}"
    elif method.value == "PUT":
        method_print = f"{Fore.YELLOW}{method.value}{Fore.RESET}"
    else:
        method_print = f"{Fore.BLUE}{method.value}{Fore.RESET}"
    print(f"➕ {Style.BRIGHT + 'route'}: {method_print} '{path}' -> {fun.__name__}")


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


def invalid_path_404(path: str, ip_address: str, method: str, log_file: str) -> None:
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
        f"❌ {Fore.RED + Style.BRIGHT + '404'} {method} {Style.BRIGHT + path} from {ip_address}"
    )
    with open(log_file, "a+") as file:
        file.write(f"❌ 404 {method} {path} from {ip_address}\n")


def valid_path_200(path: str, ip_address: str, method: str, log_file: str) -> None:
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
        f"✔ {Fore.GREEN + Style.BRIGHT + '200'} {method} {Style.BRIGHT + path} from {ip_address}"
    )
    with open(log_file, "a+") as file:
        file.write(f"✔ 200 {method} {path} from {ip_address}\n")
