import os
from functools import cache

from dotenv import load_dotenv

load_dotenv()


@cache
def get_settings(key):
    return os.getenv(key)
