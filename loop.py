import concurrent.futures

import src.storing

print("Service started...")

try:

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

            job1 = executor.submit(src.storing.refresh_exchanges_btc)
            job2 = executor.submit(src.storing.refresh_exchanges_eth)
            job3 = executor.submit(src.storing.refresh_exchanges_sol)
            job1.result()
            job2.result()
            job3.result()


except KeyboardInterrupt:
    print("Interrupt..")
