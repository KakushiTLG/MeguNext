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


def eco(sleepPlayer):
    if (sleepPlayer - 84600)  > time.time() : e=False
    else: e=True 
    return e


def hotel():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location = 'Город' AND position = 'Номер в отеле' AND energy < 99 OR location = 'Хэвенбург' AND position = 'Номер в отеле' AND energy < 99"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            nowenergy = dict['energy']
            newenergy = nowenergy + 5
            if newenergy >= 100:
                newenergy = 100
            sql = "UPDATE users SET energy = %s WHERE user_id = %s"
            cursor.execute(sql, (newenergy, dict['user_id']))
            db.commit()
            if newenergy == 100:
                try:
                    bot.send_message(dict['user_id'], "Отдохнув, ты почувствовал себя гораздо лучше. Энергия восстановлена.")
                except:
                    pass
        db.close()


def onsen():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location = 'Город' AND position = 'Источники' OR location = 'Хэвенбург' AND position = 'Источники'"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            nowenergy = dict['nowhp']
            newenergy = nowenergy + int(dict['hp'] * 0.1)
            if newenergy >= dict['hp']:
                newenergy = dict['hp']
            sql = "UPDATE users SET nowhp = %s WHERE user_id = %s"
            cursor.execute(sql, (newenergy, dict['user_id']))
            db.commit()
            if newenergy == dict['hp']:
                try:
                    sql = "UPDATE users SET position = 'Отель' WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    bot.send_message(dict['user_id'], "Отдохнув, ты почувствовал себя гораздо лучше. Здоровье восстановлено.")
                except:
                    pass
        db.close()


def minusNrg():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            if dict['location'] == 'Город' and dict['position'] == 'Номер в отеле' or dict['location'] == 'Хэвенбург' and dict['position'] == 'Номер в отеле':
                pass
            else:
                if dict['energy'] > 0:
                    e = eco(dict['sleepPlayer'])
                    if e == True: minusNrg = 1
                    else: minusNrg = 2 
                    nowenergy = dict['energy']
                    newenergy = nowenergy - minusNrg
                    if newenergy < 0:
                        newenergy = 0
                    sql = "UPDATE users SET energy = %s WHERE user_id = %s"
                    cursor.execute(sql, (newenergy, dict['user_id']))
                    db.commit()
                    if newenergy == 0:
                        try:
                            bot.send_message(dict['user_id'], "Ты полностью истощён. Если не поешь и не отдохнешь, то можешь умереть.")
                        except:
                            pass
                else:
                    newHp = dict['nowhp'] - 2
                    if newHp <= 0:
                        loser = int(dict['money'] * 0.5)
                        gorod = 'Город'
                        print("Dead")
                        text = "\nТы умер от голода. \nЗа возрождение в городе изъято {}💰".format(str(loser))
                        if dict['location'] != 'Город' and dict['location'] != 'Свалка' and dict['location'] != 'Пустыня':
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                        else:
                            sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                        sql = "UPDATE users SET position = 'Номер в отеле' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET battleStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET eat = 100 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET energy = 100 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET money = %s WHERE user_id = %s"
                        cursor.execute(sql, (loser, dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET nowhp = hp WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        try:
                        	bot.send_message(dict['user_id'], text)
                        except:
                        	pass
                    else:
                        sql = "UPDATE users SET nowhp = %s WHERE user_id = %s"
                        cursor.execute(sql, (newHp, dict['user_id']))
                        db.commit()
        db.close()


def minuseat():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            e = eco(dict['sleepPlayer'])
            if e == True: minusNrg = 2
            else: minusNrg = 3 
            if dict['eat'] > 0:
                nowenergy = dict['eat']
                newenergy = nowenergy - minusNrg
                if newenergy < 0:
                    newenergy = 0
                    print("Eat = 0")
                if dict['energy'] <= 90:
                    sql = "UPDATE users SET eat = %s WHERE user_id = %s"
                    cursor.execute(sql, (newenergy, dict['user_id']))
                    db.commit()
                    sql = "UPDATE users SET energy = energy + 3 WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    if newenergy > 15 and newenergy < 18:
                        try:
                            bot.send_message(dict['user_id'], "Ты проголодался. Если не поешь, энергия начнёт стремительно падать и спровоцирует потерю здоровья")
                        except:
                            pass
                else:
                    pass
        db.close()


def passiveArts():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM inventory WHERE name = 'Амулет здоровья' AND active = 2"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for dict in result:
                sql = "SELECT * FROM users WHERE id = %s"
                cursor.execute(sql, (dict['idplayer']))
                player = cursor.fetchone()
                if player['energy'] >= 3 and player['nowhp'] < player['hp']:
                    sql = "UPDATE users SET energy = energy - 3 WHERE user_id = %s"
                    cursor.execute(sql, (player['user_id']))
                    db.commit()
                    if player['nowhp'] + 5 > player['hp']:
                        sql = "UPDATE users SET nowhp = hp WHERE user_id = %s"
                        cursor.execute(sql, (player['user_id']))
                        db.commit()
                    else:
                        sql = "UPDATE users SET nowhp = nowhp + 5 WHERE user_id = %s"
                        cursor.execute(sql, (player['user_id']))
                        db.commit()
        sql = "SELECT * FROM inventory WHERE name = 'Осколок энергии' AND active = 2"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for dict in result:
                sql = "SELECT * FROM users WHERE id = %s"
                cursor.execute(sql, (dict['idplayer']))
                player = cursor.fetchone()
                if player['energy'] >= 10 and player['energy'] <= 60:
                    sql = "UPDATE users SET energy = energy + 5 WHERE user_id = %s"
                    cursor.execute(sql, (player['user_id']))
                    db.commit()
                    if player['energy'] + 5 >= 60:
                        sql = "UPDATE users SET energy = 60 WHERE user_id = %s"
                        cursor.execute(sql, (player['user_id']))
                        db.commit()
        db.close()




passiveArts()
hotel()
onsen()
minusNrg()
minuseat()