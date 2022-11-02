import concurrent.futures
from time import perf_counter, sleep

import src.storing

print("Service started...")

try:

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            t1_start = perf_counter()
            job1 = executor.submit(src.storing.refresh_exchanges_btc)

            job2 = executor.submit(src.storing.refresh_exchanges_eth)
            job1.result(timeout=500)
            job2.result(timeout=500)
            t1_end = perf_counter() - t1_start
            if 30 > (t1_end):
                sleep(20)

except KeyboardInterrupt:
    print("Interrupt..")
