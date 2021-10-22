import datetime as dt
import sqlite3
def test(): 
    message = "напомни мне 16.10.2021 в 8:00 сходить в школу, завтра"
    words = message.split()
    date = words[2]
    time = words[4]
    taskname = " ".join(words[5:])
    remind_flag = " ".join(words[:2])
    print(remind_flag, date, time, taskname)



def db_table_val(user: int, date: str, taskname: str):
    with sqlite3.connect('database.db') as connection:
        connection.execute('INSERT INTO alert (user, date, taskname) VALUES (?, ?, ?)', (user, date, taskname))


def alert_read():
    current_dt = dt.datetime.now()
    with sqlite3.connect('database.db') as connection:
        alerts = connection.execute('select * from alert where datetime>?', (str(current_dt),))
        print(list(alerts))
alert_read()