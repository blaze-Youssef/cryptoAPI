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

s = requests.Session()
symbols_btc = [
    x["symbol_id"]
    for x in api_call(
        "/v1/symbols?filter_symbol_id=BTC_USD&filter_exchange_id=DERIBIT", s
    )
    if "OPT" in x["symbol_id"] and int(x["symbol_id"].split("_")[4]) >= 210000
]


symbols_sol = [
    x["symbol_id"]
    for x in api_call(
        "/v1/symbols?filter_symbol_id=SOL_USD&filter_exchange_id=DERIBIT", s
    )
    if "OPT" in x["symbol_id"] and int(x["symbol_id"].split("_")[4]) >= 210000
]


symbols_eth = [
    x["symbol_id"]
    for x in api_call(
        "/v1/symbols?filter_symbol_id=ETH_USD&filter_exchange_id=DERIBIT", s
    )
    if "OPT" in x["symbol_id"] and int(x["symbol_id"].split("_")[4]) >= 210000
]


all_symbols = symbols_btc + symbols_eth + symbols_sol
