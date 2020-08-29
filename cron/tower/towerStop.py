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
        sql = "UPDATE system SET value = 0 WHERE name = 'nav_fraka'"
        cursor.execute(sql)
        db.commit()
    db.close()
a()