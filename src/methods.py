import json
import typing
from datetime import datetime
from functools import cache
from typing import Dict, List, Tuple

from starlette.responses import Response

from schemas.schemas import response
from src.storing import symbols_btc, symbols_eth

FREQUENCIES_IDS: Dict[int, str] = {1: "1min", 2: "1day"}


@cache
def get_freq_id(frequency: str) -> int:
    frequency = frequency.lower()
    for id, freq in FREQUENCIES_IDS.items():
        if freq == frequency:
            return id
    raise Exception(f"Can't find Frequency ID for {frequency}")


@cache
def get_freq(id: int) -> str:
    if id in FREQUENCIES_IDS.keys():
        return FREQUENCIES_IDS[id]
    raise Exception(f"Can't find Frequency for {id}")


@cache
def get_all_frequencies() -> Tuple[Tuple]:
    return tuple(FREQUENCIES_IDS.items())


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


@cache
def list_symbols(f: str):
    if f:
        return [x for x in symbols_btc if f.lower() in x.lower()] + [
            x for x in symbols_eth if f.lower() in x.lower()
        ]
    return symbols_eth + symbols_btc


response_search_model: Dict = {
    200: {
        "description": "List of availabe matches.",
        "model": List[response],
        "content": {
            "application/json": {
                "example": [
                    {
                        "symbol_id": "COINBASE_SPOT_BTC_USD",
                        "time_period_start": "2022-05-01T00:00:00",
                        "time_period_end": "2022-05-01T00:01:00",
                        "time_open": "2022-05-01T00:00:00",
                        "time_close": "2022-05-01T00:01:00",
                        "price_open": 37640.4,
                        "price_high": 37677.3,
                        "price_low": 37619.4,
                        "price_close": 37658.5,
                        "volume_traded": 31.2782,
                        "trades_count": 821,
                    }
                ]
            }
        },
    }
}
