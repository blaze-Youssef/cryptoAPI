import src.storing

print("Service started...")
while True:
    try:

        src.storing.refresh_exchanges()

    except BaseException as e:
        print(e)
