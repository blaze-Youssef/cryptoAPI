import concurrent.futures

import src.storing

print("Service started...")

try:

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            jobs = []
            jobs.append(executor.submit(src.storing.refresh_exchanges_btc))
            jobs.append(executor.submit(src.storing.refresh_exchanges_eth))
            jobs.append(executor.submit(src.storing.refresh_exchanges_sol))
            for job in jobs:
                job.result()


except KeyboardInterrupt:
    print("Interrupt..")
