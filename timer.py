import schedule
import time
def send_message():
    print("...")
schedule.every(1).seconds.do(send_message)
while True:
    schedule.run_pending()
    time.sleep(1)    