import pymysql
import telebot
import os
from telebot import types
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
import random
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
t = {}
tc = {}
def check():
    global t
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM trades WHERE status = 1 AND star != 0 OR status = 1 AND star2 != 0"
        cursor.execute(sql)
        trades = cursor.fetchall()
        for z in trades:
            try:
                if tc[z['fromP']]:
                    pass
            except:
                tc[z['fromP']] = 0
            try:
                if tc[z['toP']]:
                    pass
            except:
                tc[z['toP']] = 0
            try:
                if z['star2'] != 0:
                    tc[z['fromP']] += 1 
                    t[z['fromP']] += z['star2']
            except:
                if z['star2']:
                    t[z['fromP']] = z['star2']
                    tc[z['fromP']] = 1
            if z['itemreturn']:
                try:
                    if z['star'] != 0: tc[z['toP']] += 1
                    if t[z['toP']]:
                        t[z['toP']] += z['star']
                except:
                    t[z['toP']] = z['star']
        for z in t:
            sql = "SELECT tradecount, tradenum, user_id FROM users WHERE id = %s"
            cursor.execute(sql, (z))
            res = cursor.fetchone()
            allStars = t[z]
            allCount = tc[z]
            if allCount == 0:
                newLevel = 3
            else:
                newLevel = allStars / allCount
                if newLevel >= 4.9:
                	newLevel = 5
                else:
                	newLevel = int(allStars / allCount)
            print("{} - {}".format(res['user_id'], newLevel))
            if newLevel == 0: newLevel = 1
            if newLevel > res['tradenum']:
                try:
                    pass
                    bot.send_message(res['user_id'], "Ваш уровень доверия (трейды) был повышен.")
                except:
                    import traceback
                    print(str(traceback.format_exc()))
            if newLevel < res['tradenum']:
                try:
                    pass
                    bot.send_message(res['user_id'], "Ваш уровень доверия (трейды) был понижен.")
                except:
                    import traceback
                    print(str(traceback.format_exc()))
            sql = "UPDATE users SET tradenum = %s WHERE id = %s"
            cursor.execute(sql, (newLevel, z))
            db.commit()
check()