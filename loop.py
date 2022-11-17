import concurrent.futures

import src.storing

print("Service started...")

try:

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

            job1 = executor.submit(src.storing.refresh_exchanges_btc)
            job2 = executor.submit(src.storing.refresh_exchanges_eth)
            job3 = executor.submit(src.storing.refresh_exchanges_sol)
            job1.result(timeout=500)
            job2.result(timeout=500)
            job3.result(timeout=500)


except KeyboardInterrupt:
    print("Interrupt..")
