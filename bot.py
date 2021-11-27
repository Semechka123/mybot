import sqlite3
import telebot
import datetime
import schedule
import time
from threading import Thread

with open("token.txt") as f:
    token=f.readline() 
    
bot = telebot.TeleBot(token)

def user_write(user_id: int, user_name: str, user_surname: str, username: str):
    with sqlite3.connect('database.db') as connection:
        
        try:
            connection.execute('INSERT INTO user (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
            isold = False
        except(sqlite3.IntegrityError):
            isold = True 
        return isold

        
def alert_write(user: int, datetime: str, taskname: str):
    with sqlite3.connect('database.db') as connection:
             
        try:
            connection.execute('INSERT INTO alert (user, datetime, taskname) VALUES (?, ?, ?)', (user, datetime, taskname))
            query_flag = True
        except:
            query_flag = False
        return query_flag


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

		
    isold=user_write(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    if message.text.lower() == "привет":
        if isold: 
            bot.send_message(message.from_user.id, "Привет, {}!".format(us_name))
        else:
            bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text.lower() == "пока": 
        bot.send_message(message.from_user.id, "пока, {}!".format(us_name))
    elif " ".join(message.text.lower().split()[:2]) == "напомни мне":
        try:
            words = message.text.lower().split()
            date = words[2]
            format_date = "%d.%m.%Y"
            time = words[4]
            format_time = "%H:%M"
            taskname = " ".join(words[5:])
            date_v = datetime.datetime.strptime(date, format_date) 
            time_v = datetime.datetime.strptime(time, format_time).time()
            date_time = datetime.datetime.combine(date_v, time_v)
            assert date_time>datetime.datetime.now()
            dt = str(date_time)
            result = alert_write(us_id, dt, taskname)
        except(IndexError, ValueError, AssertionError):
            result = False
        if result:
            bot.send_message(message.from_user.id, "Ок")
        else:
            bot.send_message(message.from_user.id, "Формат напоминания: напомни мне 16.10.2021 в 08:00 сходить в школу")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


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

def send_message():
    alerts = alert_read()
    if alerts == None:
        print("Запрос не выполнен")
    else:
        for element in alerts:
            bot.send_message(element[1], element[3])


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)    


schedule.every(1).minutes.do(send_message)
Thread(target=schedule_checker).start() 

bot.polling(none_stop=True, interval=1)