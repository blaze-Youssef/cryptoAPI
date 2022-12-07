from requests import Session

from .conf import api_call

s = Session()
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
