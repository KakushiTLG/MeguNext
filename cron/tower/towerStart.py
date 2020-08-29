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
        sql = "UPDATE users SET progLoc = 'Первый этаж башни|0' WHERE location = 'Первый этаж башни' OR location = 'Второй этаж башни' OR location = 'Третий этаж башни' OR location = 'Четвёртый этаж башни'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET location = 'Первый этаж башни' WHERE progLoc = 'Первый этаж башни|0'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET progStatus = 1 WHERE progLoc = 'Первый этаж башни|0'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE fraks SET goldAward = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE fraks SET expAward = 0"
        cursor.execute(sql)
        db.commit()
    db.close()
a()