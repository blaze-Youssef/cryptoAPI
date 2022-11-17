import json
import typing
from functools import cache
from typing import Dict, List, Tuple

from starlette.responses import Response

from schemas.schemas import response
from src.conf import FREQUENCIES_IDS, all_symbols


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
def list_symbols(f: str | None):
    if f:
        f = f.lower()
        return [x for x in all_symbols if f in x.lower()]
    return all_symbols


@cache
def list_periods(f: str | None) -> List[str]:
    if f:
        f = f.lower()
        return [x for x in FREQUENCIES_IDS.values() if f in x.lower()]
    return list(map(str.upper, FREQUENCIES_IDS.values()))


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
