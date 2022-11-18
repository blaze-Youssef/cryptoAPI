import concurrent.futures
from time import sleep

import src.storing

print("Service started...")
CHECKFORERRORS = 60 * 5
try:

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

        job1 = executor.submit(src.storing.refresh_exchanges_btc)
        job2 = executor.submit(src.storing.refresh_exchanges_eth)
        job3 = executor.submit(src.storing.refresh_exchanges_sol)
        while True:
            sleep(CHECKFORERRORS)
            if job1.done():
                job1 = executor.submit(src.storing.refresh_exchanges_btc)
            if job2.done():
                job2 = executor.submit(src.storing.refresh_exchanges_eth)
            if job3.done():
                job3 = executor.submit(src.storing.refresh_exchanges_sol)


except KeyboardInterrupt:
    print("Interrupt..")
