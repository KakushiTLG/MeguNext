import pymysql
import telebot
import os
import random
import time
token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
def on_db():
    db = pymysql.connect(host='localhost',
                         user='rabbit',
                         password='password',                             
                         db='megu',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    return db
def a():
    db = on_db()
    with db.cursor() as cursor:
        sql = "UPDATE users SET progLoc = 'Первый этаж башни|0' WHERE location = 'Башня' OR location = 'Тропа к башне' AND progLoc = 'Тропа к башне|11'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET progStatus = 1 WHERE progLoc = 'Первый этаж башни|0'"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT * FROM users WHERE location = 'Башня'"
        cursor.execute(sql)
        result = cursor.fetchall()
        for z in result:
            try:
                bot.send_message(z['user_id'], "Вы зашли на первый этаж башни")
            except:
                pass
        sql = "UPDATE users SET location = 'Первый этаж башни' WHERE location = 'Башня'"
        cursor.execute(sql)
        db.commit()
    db.close()
a()