import os
from pathlib import Path

ASSETS: str = f"{Path(__file__).parent.parent.absolute()}{os.sep}assets"

USER_ICON: str = f"{ASSETS}{os.sep}user.svg"
