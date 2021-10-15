import sqlite3

import telebot

with open("token.txt") as f:
    token=f.readline() 
    
bot = telebot.TeleBot(token)

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    with sqlite3.connect('database.db') as connection:
        
        try:
            connection.execute('INSERT INTO user (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
            isold = False
        except(sqlite3.IntegrityError):
            isold = True 
        return isold
        
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
		
    isold=db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    if message.text.lower() == "привет":
        if isold: 
            bot.send_message(message.from_user.id, "Привет, {}!".format(us_name))
        else:
            bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text.lower() == "пока": 
        bot.send_message(message.from_user.id, "Я буду скучать, {}!".format(us_name))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
