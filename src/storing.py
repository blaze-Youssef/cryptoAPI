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
from typing import Dict, List

import requests
from dateutil import parser
from sqlalchemy import func

from src.database import Assetbtc, Asseteth, Assetsol
from src.database import scoped_Session as Session

from .conf import symbols_btc, symbols_eth, symbols_sol
from .methods import get_all_frequencies, get_freq, get_freq_id

INITIAL_DATETIME_DEF: str = get_settings("INITIAL_DATETIME_DEF")
LIMIT = get_settings("LIMIT")
request_session = None


def api_call(path) -> List[Dict]:
    global request_session
    Exc: BaseException = BaseException("Error!")
    if not request_session:
        request_session = requests.Session()
    url = f"https://rest.coinapi.io{path}"
    for _ in (0, 1):
        try:
            response = request_session.get(
                url,
                headers={"X-CoinAPI-Key": get_settings("COIN_API")},
            ).json()
        except BaseException as e:
            Exc = e
        else:
            return response
    raise Exc


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
    Session.begin()
    for freq_id, freq in get_all_frequencies():
        freq = freq.upper()
        try:

            # Get Last update time for all BTC
            query = (
                Session.query(Assetbtc.symbol_id, func.max(Assetbtc.time_period_end))
                .where(Assetbtc.frequency == freq_id)
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
                        f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}"
                    )
                    for data_bt in data_btc:
                        obj = Assetbtc(
                            symbol_id=symbol_id,
                            time_period_start=parser.parse(
                                data_bt["time_period_start"]
                            ),
                            time_period_end=parser.parse(data_bt["time_period_end"]),
                            time_open=parser.parse(data_bt["time_open"]),
                            time_close=parser.parse(data_bt["time_close"]),
                            price_open=data_bt["price_open"],
                            price_high=data_bt["price_high"],
                            price_low=data_bt["price_low"],
                            price_close=data_bt["price_close"],
                            volume_traded=data_bt["volume_traded"],
                            trades_count=data_bt["trades_count"],
                            frequency=freq_id,
                        )
                        objs.append(obj)

            Session.add_all(objs)
            Session.commit()
        except KeyboardInterrupt:
            print("Interrupt..")
        except Exception as e:
            print(e)
            sentry_sdk.capture_exception(e)
        except:
            sentry_sdk.capture_exception()

    Session.close()


def refresh_exchanges_eth():
    Session.begin()
    for freq_id, freq in get_all_frequencies():
        freq = freq.upper()
        try:

            # Get Last update time for all ETH
            query = (
                Session.query(Asseteth.symbol_id, func.max(Asseteth.time_period_end))
                .where(Asseteth.frequency == freq_id)
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
                        f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}"
                    )
                    for data_bt in data_eth:
                        obj = Asseteth(
                            symbol_id=symbol_id,
                            time_period_start=parser.parse(
                                data_bt["time_period_start"]
                            ),
                            time_period_end=parser.parse(data_bt["time_period_end"]),
                            time_open=parser.parse(data_bt["time_open"]),
                            time_close=parser.parse(data_bt["time_close"]),
                            price_open=data_bt["price_open"],
                            price_high=data_bt["price_high"],
                            price_low=data_bt["price_low"],
                            price_close=data_bt["price_close"],
                            volume_traded=data_bt["volume_traded"],
                            trades_count=data_bt["trades_count"],
                            frequency=freq_id,
                        )
                        objs.append(obj)

            Session.add_all(objs)
            Session.commit()
        except KeyboardInterrupt:
            print("Interrupt..")
        except Exception as e:
            print(e)
            sentry_sdk.capture_exception(e)
        except:
            sentry_sdk.capture_exception()
    Session.close()


def refresh_exchanges_sol():
    Session.begin()
    for freq_id, freq in get_all_frequencies():
        freq = freq.upper()
        try:

            # Get Last update time for all SOL
            query = (
                Session.query(Assetsol.symbol_id, func.max(Assetsol.time_period_end))
                .where(Assetsol.frequency == freq_id)
                .group_by(Assetsol.symbol_id)
                .order_by(func.max(Assetsol.time_period_end).desc())
            )
            data_b = query.all()
            objs = []
            for i in (1, 2):
                if i == 2:
                    data_b = [
                        (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                        for x in set(symbols_sol) - set([x[0] for x in data_b])
                    ]
                for symbol_id, enddatetime in data_b:

                    data_sol = api_call(
                        f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}"
                    )
                    for data_bt in data_sol:
                        obj = Assetsol(
                            symbol_id=symbol_id,
                            time_period_start=parser.parse(
                                data_bt["time_period_start"]
                            ),
                            time_period_end=parser.parse(data_bt["time_period_end"]),
                            time_open=parser.parse(data_bt["time_open"]),
                            time_close=parser.parse(data_bt["time_close"]),
                            price_open=data_bt["price_open"],
                            price_high=data_bt["price_high"],
                            price_low=data_bt["price_low"],
                            price_close=data_bt["price_close"],
                            volume_traded=data_bt["volume_traded"],
                            trades_count=data_bt["trades_count"],
                            frequency=freq_id,
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
