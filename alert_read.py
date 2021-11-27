import sqlite3
import datetime
import schedule
import time
from threading import Thread
def alert_read():
    with sqlite3.connect('database.db') as connection:
        
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+':00'
            print(current_time)
            all_alert = connection.execute('select * from alert where datetime =:current_time', {'current_time': current_time})
            result = all_alert.fetchall()
        except(sqlite3.IntegrityError, ValueError):
            result = None
        return result
alert_read()
# def send_message():
#     print(alert_read())


# def schedule_checker():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)    

# schedule.every(1).minutes.do(send_message)
# Thread(target=schedule_checker).start() 

##[(,,,),]
##"%d.%m.%Y"
##"%H:%M"
#[[,,,], [,,,], [,,,]]
#[,,,]
