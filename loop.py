import concurrent.futures
from time import sleep

import src.storing
from src.methods import setup_logger

logger = setup_logger(
    "loop_logger",
    "./log/loop.txt",
)

print("Service started...")
logger.info("Service started.")
CHECKFORERRORS = 60 * 5
try:

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

        job1 = executor.submit(src.storing.refresh_exchanges_btc)
        job2 = executor.submit(src.storing.refresh_exchanges_eth)
        job3 = executor.submit(src.storing.refresh_exchanges_sol)
        logger.info("Jobs submitted successfuly.")
        while True:
            sleep(CHECKFORERRORS)
            if job1.done():
                job1 = executor.submit(src.storing.refresh_exchanges_btc)
                logger.error("BTC job ended, resubmitted successfuly.")

            if job2.done():
                job2 = executor.submit(src.storing.refresh_exchanges_eth)
                logger.error("ETH job ended, resubmitted successfuly.")
            if job3.done():
                job3 = executor.submit(src.storing.refresh_exchanges_sol)
                logger.error("SOL job ended, resubmitted successfuly.")


except KeyboardInterrupt:
    print("Interrupt..")
    logger.info("Interrupt..")
