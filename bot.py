# -*- coding: utf-8 -*-
# coding: utf-8
import re
import telebot
import json
import time
from os.path import exists
from telebot.apihelper import ApiException
import logging
import os
import math
from threading import Timer
from telebot import apihelper
from telebot import types
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
import engine as db
import peewee
import random
import pymysql
import datetime
import asyncio
kakushigoto = 702528084
devChat = -1001364436303
owner = ['702528084', '405790802', '490377270']
tradeChat = -1001317123616
token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
_print = print
log = open('log.txt', 'a')
def myprint(*args, **kwargs):
    _print(*args, **kwargs)
    try:
        log.write('\t'.join(str(v) for v in args))
        log.write('\n')
        log.flush()
    except:
        pass
print = myprint 
def listener3(messages):
    for m in messages:
        dtime = datetime.datetime.fromtimestamp(int(time.time()))
        print('%s | %s[%s]:%s' % (dtime, m.from_user.first_name, m.chat.id, m.text if m.text else m.content_type))
bot.set_update_listener(listener3)
bot.send_message(kakushigoto, 'Bot started.')
bot.remove_webhook()

#Подхват файлов
game_plugins = [ f[:-3] for f in os.listdir('game') if f.endswith('.py') ]
for plugin in game_plugins:
    try:
        exec(open("./game/" + plugin + ".py", encoding="utf-8").read())
        print ("Подключен " + plugin)
    except Exception as e:
        print("Ошибка подключения " + plugin) 
try:
    exec(open("./main.py", encoding="utf-8").read())
except Exception as e:
    print(e)
import engine as e
# !

def databasetimer():
    if not db.database.is_closed():
        db.database.close()
    db.database.connect()
    print("DB conn restart")
t = Timer(3600, databasetimer, [])
t.start()
import traceback
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(kakushigoto, str(traceback.format_exc()))
        print('\n\nRestart\n\n')
        time.sleep(1)
        
