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
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        for z in result:
            sql = "INSERT INTO inventory (name, Type, bonus, size, active, idplayer) VALUES ('Сун-дук', 'Сундук', 0, 1, 1, %s)"
            cursor.execute(sql, (z['id']))
            db.commit()
    db.close()
a()