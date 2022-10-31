from datetime import datetime
from typing import List

import sentry_sdk
from dateutil import parser
from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from schemas.schemas import SYMBOL_ID, response
from src.conf import get_settings
from src.database_api import scoped_Session
from src.methods import list_symbols, response_search_model
from src.search import search
from src.storing import INITIAL_DATETIME_DEF

sentry_sdk.init(
    dsn=get_settings("DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)
app = FastAPI()


def get_db():
    db = scoped_Session()
    try:
        yield db
    finally:
        db.close()


def my_schema():
    openapi_schema = get_openapi(
        title="Crypto Data API",
        version="1.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/v1/ohlcv/{symbol_id}/history", responses=response_search_model)
async def history(
    symbol_id: str,
    time_start: datetime = parser.parse(INITIAL_DATETIME_DEF),
    time_end: datetime = datetime.now(),
    limit=100,
    Session=Depends(get_db),
) -> List[response]:
    symbol_id = SYMBOL_ID(symbol_id=symbol_id, type=0)

    return await search(symbol_id, time_start, time_end, limit, Session)


@app.get("/v1/ListSymbols")
def listymbols(Filter: str = None):
    return list_symbols(Filter)


app.openapi = my_schema
