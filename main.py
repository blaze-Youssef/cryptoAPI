import sentry_sdk

from src.conf import get_settings

sentry_sdk.init(
    dsn=get_settings("DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

from datetime import datetime
from typing import List

from dateutil import parser
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from schemas.schemas import SYMBOL_ID, response
from src.conf import get_settings
from src.database import scoped_Session
from src.methods import (
    PrettyJSONResponse,
    list_periods,
    list_symbols,
    response_search_model,
)
from src.search import search
from src.storing import INITIAL_DATETIME_DEF

app = FastAPI(
    title="Crypto Data API",
    version="1.0",
    description="API to get OHLCV (Open, High, Low, Close, Volume) timeseries data. Each data point of this timeseries represents several indicators calculated from transactions activity inside a time range (period).",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url=None,
)
app.mount("/ressources", StaticFiles(directory="./ressources"), name="ressources")


def get_db():
    db = scoped_Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Crypto Data API",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        swagger_favicon_url="/ressources/favicon.ico",
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get(
    "/v1/ohlcv/{symbol_id}/history",
    responses=response_search_model,
    description="Get OHLCV timeseries data returned in time ascending order. Data can be requested by the period and for the specific symbol eg BITSTAMP_SPOT_BTC_USD, if you need to query timeseries by asset pairs eg. BTC/USD, then please reffer to the Exchange Rates Timeseries data",
)
async def history(
    API_KEY: str = Query(..., description="Authentication token"),
    symbol_id: str = Path(
        ...,
        description="Symbol identifier of requested timeseries (full list available [here](/v1/ListSymbols))",
    ),
    time_start: datetime = Query(
        default=parser.parse(INITIAL_DATETIME_DEF),
        description="Timeseries starting time in ISO 8601 (optional, if not supplied the default value is 2022-05-01T00:00:00)",
    ),
    time_end: datetime = Query(
        default=datetime.now(),
        description="Timeseries ending time in ISO 8601 (optional, if not supplied then the data is returned to the end or when count of result elements reaches the limit)",
    ),
    period_id: str = Query(
        default="1MIN",
        description="Identifier of requested timeseries period [here](/v1/periods)",
    ),
    limit: int = Query(
        default=100,
        description="Amount of items to return (optional, mininum is 1, maximum is 100000, default value is 100.",
        ge=1,
        le=100000,
    ),
    Session=Depends(get_db),
) -> List[response]:
    if not API_KEY == get_settings("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    symbol: SYMBOL_ID = SYMBOL_ID(symbol_id=symbol_id, type=0)

    return await search(symbol, time_start, time_end, limit, Session, period_id)


@app.get("/v1/ListSymbols", response_class=PrettyJSONResponse)
def listymbols(Filter: (str | None) = None) -> List[str]:
    return list_symbols(Filter)


@app.get("/v1/periods", response_class=PrettyJSONResponse)
def listperiods(Filter: (str | None) = None) -> List[str]:
    return list_periods(Filter)
