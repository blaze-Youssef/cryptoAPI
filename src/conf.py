import os
from functools import cache
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv(override=True)


@cache
def get_settings(key: str) -> str:
    val = os.getenv(key)
    if val:
        return str(val)
    raise Exception(f"Environement variable not found {key}.")


def api_call(path, request_session=None) -> List[Dict]:
    Exc: BaseException = BaseException("Error!")
    if not request_session:
        request_session = requests.Session()
    url = f"https://rest.coinapi.io{path}"
    for _ in (0, 1):
        try:
            response = request_session.get(
                url,
                headers={"X-CoinAPI-Key": get_settings("COIN_API")},
            ).json()
        except BaseException as e:
            Exc = e
        else:
            return response
    raise Exc


FREQUENCIES_IDS: Dict[int, str] = {1: "1day"}
