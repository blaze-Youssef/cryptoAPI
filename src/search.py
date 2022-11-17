from datetime import datetime
from typing import List

from fastapi import HTTPException
from pymysql import OperationalError
from sqlalchemy.orm.session import Session as Session_int

from schemas.schemas import SYMBOL_ID, response
from src.database import Assetbtc, Asseteth, Assetsol

from .methods import get_freq_id


async def search(
    symbol_id: SYMBOL_ID,
    time_start: datetime,
    time_end: datetime,
    limit,
    Session: Session_int,
    frequency: str,
) -> List[response]:
    period_id: int = get_freq_id(frequency)
    data = []
    try:
        if symbol_id.type == 0:
            data = (
                Session.query(Assetbtc)
                .where(Assetbtc.frequency == period_id)
                .where(Assetbtc.symbol_id == symbol_id.symbol_id)
                .where(time_start <= Assetbtc.time_period_start)
                .where(time_end >= Assetbtc.time_period_end)
                .limit(limit)
                .all()
            )
        elif symbol_id.type == 1:
            data = (
                Session.query(Asseteth)
                .where(Asseteth.frequency == period_id)
                .where(Asseteth.symbol_id == symbol_id.symbol_id)
                .where(time_start <= Asseteth.time_period_start)
                .where(time_end >= Asseteth.time_period_end)
                .limit(limit)
                .all()
            )
        elif symbol_id.type == 2:
            data = (
                Session.query(Assetsol)
                .where(Assetsol.frequency == period_id)
                .where(Assetsol.symbol_id == symbol_id.symbol_id)
                .where(time_start <= Assetsol.time_period_start)
                .where(time_end >= Assetsol.time_period_end)
                .limit(limit)
                .all()
            )
    except OperationalError:

        raise HTTPException(500, detail="Database error, please try again later.")
    else:
        return [response(**ss.__dict__) for ss in data]
