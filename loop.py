import concurrent.futures

import src.storing

print("Service started...")

try:

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            job1 = executor.submit(src.storing.refresh_exchanges_btc)
            job1.result(timeout=500)
            job2 = executor.submit(src.storing.refresh_exchanges_eth)

            job2.result(timeout=500)


except KeyboardInterrupt:
    print("Interrupt..")
