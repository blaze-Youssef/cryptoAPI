from datetime import datetime

import pycurl_requests as requests
from dateutil import parser
from sqlalchemy import desc

from src.database import Assetbtc, Asseteth, SessionLocal

from .conf import get_settings

INITIAL_DATETIME_DEF = get_settings("INITIAL_DATETIME_DEF")
LIMIT = get_settings("LIMIT")


symbols_btc = [
    "COINBASE_SPOT_BTC_USD",
    "BINANCEUS_SPOT_BTC_USD",
    "BINANCEFTSC_PERP_BTC_USD",
    "OKEX_PERP_BTC_USD",
    "OKEX_IDX_BTC_USD",
    "KRAKEN_SPOT_BTC_USD",
    "KRAKENFTS_PERP_BTC_USD",
    "GEMINI_SPOT_BTC_USD",
    "HUOBI_SPOT_BTC_USD",
    "HUOBIFTS_PERP_BTC_USD",
    "BITMEX_PERP_BTC_USD",
    "BYBIT_PERP_BTC_USD",
    "BYBITUSDC_PERP_BTC_USD",
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
    "HUOBI_SPOT_ETH_USD",
    "HUOBIFTS_PERP_ETH_USD",
    "BITMEX_PERP_ETH_USD",
    "BYBIT_PERP_ETH_USD",
    "BYBITUSDC_PERP_ETH_USD",
    "FTX_PERP_ETH_USD",
    "FTX_SPOT_ETH_USD",
    "FTXUS_SPOT_ETH_USD",
    "BITFINEX_SPOT_ETH_USD",
    "BITSTAMP_SPOT_ETH_USD",
]


def api_call(path) -> dict:
    return requests.get(
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
    return datetime.now().replace(microsecond=0).isoformat()


"""def add_todb_otherthread(Objs: List):
    session = scoped_Session()
    for obj in Objs:
        session.add(obj)
    session.commit()
    scoped_Session.remove()
    return True"""


def refresh_exchanges():
    Session = SessionLocal()
    try:
        for symbol_id in symbols_btc:
            last: Assetbtc = (
                Session.query(Assetbtc)
                .where(Assetbtc.symbol_id == symbol_id)
                .order_by(desc("time_period_end"))
                .first()
            )
            if last:
                INITIAL_DATETIME = last.time_period_end.isoformat()
            else:
                INITIAL_DATETIME = INITIAL_DATETIME_DEF
            data_btc = api_call(
                f"/v1/ohlcv/{symbol_id}/history?period_id=1MIN&time_start={INITIAL_DATETIME}&time_end={get_iso()}&limit={LIMIT}"
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
                Session.add(obj)
        Session.commit()

        for symbol_id in symbols_eth:
            last: Asseteth = (
                Session.query(Asseteth)
                .where(Asseteth.symbol_id == symbol_id)
                .order_by(desc("time_period_end"))
                .first()
            )
            if last:
                INITIAL_DATETIME = last.time_period_end.isoformat()
            else:
                INITIAL_DATETIME = INITIAL_DATETIME_DEF
            data_btc = api_call(
                f"/v1/ohlcv/{symbol_id}/history?period_id=1MIN&time_start={INITIAL_DATETIME}&time_end={get_iso()}&limit={LIMIT}"
            )
            for data_bt in data_btc:
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
                Session.add(obj)
        Session.commit()
        Session.close()
    except:
        Session.close()
