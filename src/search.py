from datetime import datetime

from async_lru import alru_cache
from fastapi import HTTPException
from pymysql import OperationalError
from sqlalchemy.orm.session import Session as Session_int

from schemas.schemas import SYMBOL_ID, response
from src.database import Assetbtc, Asseteth


@alru_cache(maxsize=1024)
async def search(
    symbol_id: SYMBOL_ID,
    time_start: datetime,
    time_end: datetime,
    limit,
    Session: Session_int,
):
    for i in [0, 1]:
        try:
            if symbol_id.type == 0:
                data = (
                    Session.query(Assetbtc)
                    .where(Assetbtc.symbol_id == symbol_id.symbol_id)
                    .where(time_start <= Assetbtc.time_period_start)
                    .where(time_end >= Assetbtc.time_period_end)
                    .limit(limit)
                    .all()
                )
            else:
                data = (
                    Session.query(Asseteth)
                    .where(Asseteth.symbol_id == symbol_id.symbol_id)
                    .where(time_start <= Asseteth.time_period_start)
                    .where(time_end >= Asseteth.time_period_end.time_period_end)
                    .limit(limit)
                    .all()
                )
            break
        except OperationalError:
            if i == 1:
                raise HTTPException(
                    500, detail="Database error, please try again later."
                )
    return [response(**ss.__dict__) for ss in data]
