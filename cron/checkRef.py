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

refss = {}
def refs():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        for z in result:
            sql = "SELECT * FROM users WHERE ref = %s"
            cursor.execute(sql, (z['user_id']))
            res = cursor.fetchall()
            if res:
                refss[z['username']] = 0
                for x in res:
                    refss[z['username']] += 1
        bot.send_message(702528084, str(refss))
refs()