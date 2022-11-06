import os
from functools import cache

from dotenv import load_dotenv

load_dotenv()


@cache
def get_settings(key: str) -> str:
    val = os.getenv(key)
    if val:
        return str(val)
    raise Exception(f"Environement variable not found {key}.")
