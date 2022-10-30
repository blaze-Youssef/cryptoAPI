from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, validator

from src.storing import symbols_btc, symbols_eth


class SYMBOL_ID(BaseModel):
    symbol_id: str
    type: int

    @validator("symbol_id")
    def val(cls, v):
        v = v.upper()
        if v in symbols_btc or v in symbols_eth:
            return v
        raise HTTPException(
            404, detail="Invalid parameter symbol_id. You can list all symbols in #doc"
        )

    @validator("type")
    def v(cls, v, values, **kwargs):
        if values["symbol_id"] in symbols_btc:
            return 0
        return 1

    def __hash__(self):
        return hash(self.symbol_id.lower())


class response(BaseModel):
    symbol_id: str
    time_period_start: datetime
    time_period_end: datetime
    time_open: datetime
    time_close: datetime
    price_open: float
    price_high: float
    price_low: float
    price_close: float
    volume_traded: float
    trades_count: int
