import sentry_sdk

from .conf import get_settings

sentry_sdk.init(
    dsn=get_settings("DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

from datetime import datetime, timedelta

import requests
from dateutil import parser
from sqlalchemy import func

from src.database import Assetbtc, Asseteth, engine
from src.database import scoped_Session as Session

INITIAL_DATETIME_DEF: str = get_settings("INITIAL_DATETIME_DEF")
LIMIT = get_settings("LIMIT")
request_session = None

symbols_btc = [
    "COINBASE_SPOT_BTC_USD",
    "BINANCEUS_SPOT_BTC_USD",
    "BINANCEFTSC_PERP_BTC_USD",
    "OKEX_PERP_BTC_USD",
    "OKEX_IDX_BTC_USD",
    "KRAKEN_SPOT_BTC_USD",
    "KRAKENFTS_PERP_BTC_USD",
    "GEMINI_SPOT_BTC_USD",
    "BITMEX_PERP_BTC_USD",
    "BYBIT_PERP_BTC_USD",
    "FTX_PERP_BTC_USD",
    "FTX_SPOT_BTC_USD",
    "FTXUS_SPOT_BTC_USD",
    "BITFINEX_SPOT_BTC_USD",
    "BITSTAMP_SPOT_BTC_USD",
]

symbols_eth = [
    "COINBASE_SPOT_ETH_USD",
    "BINANCEUS_SPOT_ETH_USD",
    "BINANCEFTSC_PERP_ETH_USD",
    "OKEX_PERP_ETH_USD",
    "OKEX_IDX_ETH_USD",
    "KRAKEN_SPOT_ETH_USD",
    "KRAKENFTS_PERP_ETH_USD",
    "GEMINI_SPOT_ETH_USD",
    "BITMEX_PERP_ETH_USD",
    "BYBIT_PERP_ETH_USD",
    "FTX_PERP_ETH_USD",
    "FTX_SPOT_ETH_USD",
    "FTXUS_SPOT_ETH_USD",
    "BITFINEX_SPOT_ETH_USD",
    "BITSTAMP_SPOT_ETH_USD",
]


def api_call(path) -> dict:
    global request_session
    if not request_session:
        request_session = requests.Session()
    return request_session.get(
        f"https://rest.coinapi.io{path}",
        headers={"X-CoinAPI-Key": get_settings("COIN_API")},
    ).json()


"""def refresh_assets():
    btc = api_call("/v1/exchangerate/BTC/USD")
    eth = api_call("/v1/exchangerate/ETH/USD")
    avbtc = False
    aveth = False
    if Session.query(Assets).where(Assets.id == 1).first():
        avbtc = True
    if Session.query(Assets).where(Assets.id == 1).first():
        aveth = True

    if avbtc:
        stmt = update(Assets).where(Assets.id == 1).values(rate=btc["rate"])
    else:
        stmt = insert(Assets).values(id=1, base="btc", quote="usd", rate=btc["rate"])
    engine.execute(stmt)
    if aveth:
        stmt = update(Assets).where(Assets.id == 2).values(rate=eth["rate"])
    else:
        stmt = insert(Assets).values(id=2, base="eth", quote="usd", rate=eth["rate"])
    engine.execute(stmt)
    Session.commit()

"""


def get_iso():
    return (datetime.now().replace(microsecond=0) + timedelta(minutes=1)).isoformat()


"""def add_todb_otherthread(Objs: List):
    session = scoped_Session()
    for obj in Objs:
        session.add(obj)
    session.commit()
    scoped_Session.remove()
    return True"""


def refresh_exchanges_btc():

    try:

        Session.begin()
        # Get Last update time for all BTC
        query = (
            Session.query(Assetbtc.symbol_id, func.max(Assetbtc.time_period_end))
            .group_by(Assetbtc.symbol_id)
            .order_by(func.max(Assetbtc.time_period_end).desc())
        )
        data_b = query.all()
        objs = []
        for i in (1, 2):
            if i == 2:
                data_b = [
                    (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                    for x in set(symbols_btc) - set([x[0] for x in data_b])
                ]
            for symbol_id, enddatetime in data_b:

                data_btc = api_call(
                    f"/v1/ohlcv/{symbol_id}/history?period_id=1MIN&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}"
                )
                for data_bt in data_btc:
                    obj = Assetbtc(
                        symbol_id=symbol_id,
                        time_period_start=parser.parse(data_bt["time_period_start"]),
                        time_period_end=parser.parse(data_bt["time_period_end"]),
                        time_open=parser.parse(data_bt["time_open"]),
                        time_close=parser.parse(data_bt["time_close"]),
                        price_open=data_bt["price_open"],
                        price_high=data_bt["price_high"],
                        price_low=data_bt["price_low"],
                        price_close=data_bt["price_close"],
                        volume_traded=data_bt["volume_traded"],
                        trades_count=data_bt["trades_count"],
                    )
                    objs.append(obj)

        Session.add_all(objs)
        Session.commit()
    except KeyboardInterrupt:
        print("Interrupt..")
    except Exception as e:
        print(e)
        sentry_sdk.capture_exception(e)

    Session.close()


def refresh_exchanges_eth():

    try:

        Session.begin()
        objs = []
        # Get Last update time for all eth
        query = (
            Session.query(Asseteth.symbol_id, func.max(Asseteth.time_period_end))
            .group_by(Asseteth.symbol_id)
            .order_by(func.max(Asseteth.time_period_end).desc())
        )
        data_b = query.all()
        objs = []
        for i in (1, 2):
            if i == 2:
                data_b = [
                    (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                    for x in set(symbols_eth) - set([x[0] for x in data_b])
                ]
            for symbol_id, enddatetime in data_b:

                data_eth = api_call(
                    f"/v1/ohlcv/{symbol_id}/history?period_id=1MIN&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}"
                )
                for data_bt in data_eth:
                    obj = Asseteth(
                        symbol_id=symbol_id,
                        time_period_start=parser.parse(data_bt["time_period_start"]),
                        time_period_end=parser.parse(data_bt["time_period_end"]),
                        time_open=parser.parse(data_bt["time_open"]),
                        time_close=parser.parse(data_bt["time_close"]),
                        price_open=data_bt["price_open"],
                        price_high=data_bt["price_high"],
                        price_low=data_bt["price_low"],
                        price_close=data_bt["price_close"],
                        volume_traded=data_bt["volume_traded"],
                        trades_count=data_bt["trades_count"],
                    )
                    objs.append(obj)
        Session.add_all(objs)
        Session.commit()
    except KeyboardInterrupt:

        print("Interrupt..")
    except Exception as e:
        print(e)
        sentry_sdk.capture_exception(e)
    Session.close()
