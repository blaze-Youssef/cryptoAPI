from time import sleep

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

from dateutil import parser
from sqlalchemy import func

from src.database import Assetbtc, Asseteth, Assetsol
from src.database import scoped_Session as Session

from .conf import api_call, symbols_btc, symbols_eth, symbols_sol
from .methods import get_all_frequencies, setup_logger

INITIAL_DATETIME_DEF: str = get_settings("INITIAL_DATETIME_DEF")
LIMIT = get_settings("LIMIT")


request_session = None


btc_logger = setup_logger(
    "btc_logger",
    "./log/btc.txt",
)
eth_logger = setup_logger(
    "eth_logger",
    "./log/eth.txt",
)
sol_logger = setup_logger(
    "sol_logger",
    "./log/sol.txt",
)


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
    data_db = {}
    btc_logger.info("BTC started listening for new data.")
    try:
        while True:
            sleep(10)
            for freq_id, freq in get_all_frequencies():
                freq = freq.upper()
                # Get Last update time for all BTC
                if data_db:
                    data_b = list(data_db.items())
                else:
                    query = (
                        Session.query(
                            Assetbtc.symbol_id, func.max(Assetbtc.time_period_end)
                        )
                        .where(Assetbtc.frequency == freq_id)
                        .group_by(Assetbtc.symbol_id)
                        .order_by(func.max(Assetbtc.time_period_end).desc())
                    )
                    data_b = query.all()
                    for symb, enddate in data_b:
                        data_db[symb] = enddate
                objs = []
                for i in (1, 2):
                    if i == 2:
                        data_b = [
                            (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                            for x in set(symbols_btc) - set([x[0] for x in data_b])
                        ]
                        if data_b:
                            btc_logger.debug(
                                f"BTC Noticed {len(data_b)} symbol_ids with no rows in database, checking.."
                            )
                    for symbol_id, enddatetime in data_b:

                        data_btc = api_call(
                            f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}",
                            request_session,
                        )
                        is_data = False
                        for data_bt in data_btc:
                            obj = Assetbtc(
                                symbol_id=symbol_id,
                                time_period_start=parser.parse(
                                    data_bt["time_period_start"]
                                ),
                                time_period_end=parser.parse(
                                    data_bt["time_period_end"]
                                ),
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
                            if not is_data:
                                btc_logger.debug(
                                    f"BTC {symbol_id} Found data, adding to session."
                                )
                                is_data = True
                        if is_data:
                            data_db[symbol_id] = objs[-1].time_period_end.replace(
                                tzinfo=None
                            )
                        if len(objs) == 200:
                            Session.commit()
                            objs = []
                if objs:
                    btc_logger.info(f"BTC commiting {len(objs)} rows to the database.")
                    Session.add_all(objs)
                    Session.commit()
                    btc_logger.debug(f"BTC commiting finished successfully.")
    except KeyboardInterrupt:
        print("Interrupt..")
    except Exception as e:
        print(e)
        btc_logger.error(e)
        sentry_sdk.capture_exception(e)
    except:
        sentry_sdk.capture_exception()
    Session.close()


def refresh_exchanges_eth():
    Session.begin()
    data_db = {}
    eth_logger.info("ETH started listening for new data.")
    try:
        while True:
            sleep(10)
            for freq_id, freq in get_all_frequencies():
                freq = freq.upper()
                # Get Last update time for all ETH
                if data_db:
                    data_b = list(data_db.items())
                else:
                    query = (
                        Session.query(
                            Asseteth.symbol_id, func.max(Asseteth.time_period_end)
                        )
                        .where(Asseteth.frequency == freq_id)
                        .group_by(Asseteth.symbol_id)
                        .order_by(func.max(Asseteth.time_period_end).desc())
                    )
                    data_b = query.all()
                    for symb, enddate in data_b:
                        data_db[symb] = enddate
                objs = []
                for i in (1, 2):
                    if i == 2:
                        data_b = [
                            (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                            for x in set(symbols_eth) - set([x[0] for x in data_b])
                        ]
                        if data_b:
                            eth_logger.debug(
                                f"ETH Noticed {len(data_b)} symbol_ids with no rows in database, checking.."
                            )
                    for symbol_id, enddatetime in data_b:

                        data_eth = api_call(
                            f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}",
                            request_session,
                        )
                        is_data = False
                        for data_bt in data_eth:
                            obj = Asseteth(
                                symbol_id=symbol_id,
                                time_period_start=parser.parse(
                                    data_bt["time_period_start"]
                                ),
                                time_period_end=parser.parse(
                                    data_bt["time_period_end"]
                                ),
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
                            if not is_data:
                                is_data = True
                        if is_data:
                            eth_logger.debug(
                                f"ETH {symbol_id} Found data, adding to session."
                            )
                            data_db[symbol_id] = objs[-1].time_period_end.replace(
                                tzinfo=None
                            )
                        if len(objs) == 200:
                            Session.commit()
                            objs = []

                if objs:
                    eth_logger.info(f"ETH commiting {len(objs)} rows to the database.")
                    Session.add_all(objs)
                    Session.commit()
                    eth_logger.debug(f"ETH commiting finished successfully.")
    except KeyboardInterrupt:
        print("Interrupt..")
    except Exception as e:
        print(e)
        eth_logger.error(e)
        sentry_sdk.capture_exception(e)
    except:
        sentry_sdk.capture_exception()
    Session.close()


def refresh_exchanges_sol():
    Session.begin()
    data_db = {}
    sol_logger.info("SOL started listening for new data.")
    try:
        while True:
            sleep(10)
            for freq_id, freq in get_all_frequencies():
                freq = freq.upper()

                # Get Last update time for all SOL
                if data_db:
                    data_b = list(data_db.items())
                else:
                    query = (
                        Session.query(
                            Assetsol.symbol_id, func.max(Assetsol.time_period_end)
                        )
                        .where(Assetsol.frequency == freq_id)
                        .group_by(Assetsol.symbol_id)
                        .order_by(func.max(Assetsol.time_period_end).desc())
                    )
                    data_b = query.all()
                    for symb, enddate in data_b:
                        data_db[symb] = enddate
                objs = []
                for i in (1, 2):
                    if i == 2:
                        data_b = [
                            (x, datetime.fromisoformat(INITIAL_DATETIME_DEF))
                            for x in set(symbols_sol) - set([x[0] for x in data_b])
                        ]
                        if data_b:
                            sol_logger.debug(
                                f"SOL Noticed {len(data_b)} symbol_ids with no rows in database, checking.."
                            )
                    for symbol_id, enddatetime in data_b:

                        data_sol = api_call(
                            f"/v1/ohlcv/{symbol_id}/history?period_id={freq}&time_start={enddatetime.replace(microsecond=0).isoformat()}&time_end={get_iso()}&limit={LIMIT}",
                            request_session,
                        )
                        is_data = False
                        for data_bt in data_sol:
                            obj = Assetsol(
                                symbol_id=symbol_id,
                                time_period_start=parser.parse(
                                    data_bt["time_period_start"]
                                ),
                                time_period_end=parser.parse(
                                    data_bt["time_period_end"]
                                ),
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
                            if not is_data:
                                is_data = True
                        if is_data:
                            sol_logger.debug(
                                f"SOL {symbol_id} Found data, adding to session."
                            )
                            data_db[symbol_id] = objs[-1].time_period_end.replace(
                                tzinfo=None
                            )
                        if len(objs) == 200:
                            Session.commit()
                            objs = []
                if objs:
                    sol_logger.info(f"SOL commiting {len(objs)} rows to the database.")
                    Session.add_all(objs)
                    Session.commit()
                    sol_logger.debug(f"SOL commiting finished successfully.")
    except KeyboardInterrupt:
        print("Interrupt..")
    except Exception as e:
        print(e)
        sol_logger.error(e)
        sentry_sdk.capture_exception(e)

    Session.close()
