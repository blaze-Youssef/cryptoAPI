import os
from functools import cache
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


@cache
def get_settings(key: str) -> str:
    val = os.getenv(key)
    if val:
        return str(val)
    raise Exception(f"Environement variable not found {key}.")


FREQUENCIES_IDS: Dict[int, str] = {1: "1min", 2: "1day"}

symbols_sol = [
    "DERIBIT_IDX_SOL_USD",
    "DERIBIT_PERP_SOL_USD",
]

symbols_btc = [
    "DERIBIT_PERP_BTC_USD",
    "DERIBIT_IDX_BTC_USD",
]

symbols_eth = [
    "DERIBIT_PERP_ETH_USD",
    "DERIBIT_IDX_ETH_USD",
    "DERIBIT_SPOT_ETH_USD",
]


all_symbols = symbols_btc + symbols_eth + symbols_sol
