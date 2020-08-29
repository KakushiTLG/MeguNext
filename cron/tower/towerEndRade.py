import pymysql
import telebot
import os
import random
import time
token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
tradeChat = -1001317123616

def on_db():
    db = pymysql.connect(host='localhost',
                         user='rabbit',
                         password='password',                             
                         db='megu',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    return db



def a():
    fraks = {'Вавилон': 0, 'Небесные рыцари': 0, 'Грязное небо': 0, 'Хранители': 0}
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location = 'Первый этаж башни' AND progLoc = 'Первый этаж башни|5' AND nowhp > 0"
        cursor.execute(sql)
        resultzz = cursor.fetchall()
        for z in resultzz:
            fraks[z['frak']] += (z['atk'] + z['nowhp'])
        cursor.execute('TRUNCATE `temp`')
        db.commit()
        for x in fraks:
            sql = "INSERT INTO temp (user_id, count) VALUES (%s, %s)"
            cursor.execute(sql, (x, fraks[x]))
            db.commit()
        sql = "SELECT * FROM temp ORDER BY count DESC"
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "SELECT * FROM fraks WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        rs = cursor.fetchone()
        goldAward = rs['goldAward'] + int(rs['goldAward'] * 0.05)
        expAward = rs['expAward'] + int(rs['expAward'] * 0.05)
        sql = "UPDATE fraks SET goldAward = %s WHERE name = %s"
        cursor.execute(sql, (goldAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET expAward = %s WHERE name = %s"
        cursor.execute(sql, (expAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET ametist = ametist + 3 WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        db.commit()
        for z in resultzz:
            bot.send_message(z['user_id'], "Победителем на первом этаже вышла группировка {}".format(rs['name']))
        fraks = {'Вавилон': 0, 'Небесные рыцари': 0, 'Грязное небо': 0, 'Хранители': 0}
        sql = "SELECT * FROM users WHERE location = 'Второй этаж башни' AND progLoc = 'Второй этаж башни|7' AND nowhp > 0"
        cursor.execute(sql)
        resultzz = cursor.fetchall()
        for z in resultzz:
            fraks[z['frak']] += (z['atk'] + z['nowhp'])
        cursor.execute('TRUNCATE `temp`')
        db.commit()
        for x in fraks:
            sql = "INSERT INTO temp (user_id, count) VALUES (%s, %s)"
            cursor.execute(sql, (x, fraks[x]))
            db.commit()
        sql = "SELECT * FROM temp ORDER BY count DESC"
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "SELECT * FROM fraks WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        rs = cursor.fetchone()
        goldAward = rs['goldAward'] + int(rs['goldAward'] * 0.1)
        expAward = rs['expAward'] + int(rs['expAward'] * 0.1)
        sql = "UPDATE fraks SET goldAward = %s WHERE name = %s"
        cursor.execute(sql, (goldAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET expAward = %s WHERE name = %s"
        cursor.execute(sql, (expAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET rubin = rubin + 3 WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        db.commit()
        for z in resultzz:
            bot.send_message(z['user_id'], "Победителем на втором этаже вышла группировка {}".format(rs['name']))
        fraks = {'Вавилон': 0, 'Небесные рыцари': 0, 'Грязное небо': 0, 'Хранители': 0}
        sql = "SELECT * FROM users WHERE location = 'Третий этаж башни' AND progLoc = 'Третий этаж башни|9' AND nowhp > 0"
        cursor.execute(sql)
        resultzz = cursor.fetchall()
        for z in resultzz:
            fraks[z['frak']] += (z['atk'] + z['nowhp'])
        cursor.execute('TRUNCATE `temp`')
        db.commit()
        for x in fraks:
            sql = "INSERT INTO temp (user_id, count) VALUES (%s, %s)"
            cursor.execute(sql, (x, fraks[x]))
            db.commit()
        sql = "SELECT * FROM temp ORDER BY count DESC"
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "SELECT * FROM fraks WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        rs = cursor.fetchone()
        goldAward = rs['goldAward'] + int(rs['goldAward'] * 0.15)
        expAward = rs['expAward'] + int(rs['expAward'] * 0.15)
        sql = "UPDATE fraks SET goldAward = %s WHERE name = %s"
        cursor.execute(sql, (goldAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET expAward = %s WHERE name = %s"
        cursor.execute(sql, (expAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET sapphire = sapphire + 3 WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        db.commit()
        for z in resultzz:
            bot.send_message(z['user_id'], "Победителем на третьем этаже вышла группировка {}".format(rs['name']))
        fraks = {'Вавилон': 0, 'Небесные рыцари': 0, 'Грязное небо': 0, 'Хранители': 0}
        sql = "SELECT * FROM users WHERE location = 'Четвёртый этаж башни' AND progLoc = 'Четвёртый этаж башни|11' AND nowhp > 0"
        cursor.execute(sql)
        resultzz = cursor.fetchall()
        for z in resultzz:
            fraks[z['frak']] += (z['atk'] + z['nowhp'])
        cursor.execute('TRUNCATE `temp`')
        db.commit()
        for x in fraks:
            sql = "INSERT INTO temp (user_id, count) VALUES (%s, %s)"
            cursor.execute(sql, (x, fraks[x]))
            db.commit()
        sql = "SELECT * FROM temp ORDER BY count DESC"
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "SELECT * FROM fraks WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        rs = cursor.fetchone()
        goldAward = rs['goldAward'] + int(rs['goldAward'] * 0.2)
        expAward = rs['expAward'] + int(rs['expAward'] * 0.2)
        sql = "UPDATE fraks SET goldAward = %s WHERE name = %s"
        cursor.execute(sql, (goldAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET expAward = %s WHERE name = %s"
        cursor.execute(sql, (expAward, result['user_id']))
        db.commit()
        sql = "UPDATE fraks SET izumrud = izumrud + 3 WHERE name = %s"
        cursor.execute(sql, (result['user_id']))
        db.commit()
        for z in resultzz:
            bot.send_message(z['user_id'], "Победителем на четвёртом этаже вышла группировка {}".format(rs['name']))
        sql = "SELECT * FROM fraks"
        cursor.execute(sql)
        fraks = cursor.fetchall()
        for z in fraks:
            plusExpForPlayers = int(z['expAward'] * 0.1)
            plusGoldForPlayer = int(z['goldAward'] * 0.1)
            sql = "SELECT user_id, location, lvl, exp FROM users WHERE frak = %s"
            cursor.execute(sql, (z['name']))
            allusers = cursor.fetchall()
            for x in allusers:
                if x['location'] == 'Первый этаж башни' or x['location'] == 'Второй этаж башни' or x['location'] == 'Третий этаж башни' or x['location'] == 'Четвёртый этаж башни' or x['location'] == 'Пятый этаж башни' or x['location'] == 'Шестой этаж башни' or x['location'] == 'Седьмой этаж башни':
                    if (x['lvl'] * 100) <= (x['exp'] + plusExpForPlayers):
                        sql = "UPDATE users SET lvl = lvl + 1 WHERE user_id = %s"
                        cursor.execute(sql, (x['user_id']))
                        db.commit()
                        text = "Вы получили (Новый уровень!) {}✨ и {}💰 за рейд башни".format(plusExpForPlayers, plusGoldForPlayer)
                    else:
                        sql = "UPDATE users SET exp = exp + %s WHERE user_id = %s"
                        cursor.execute(sql, (plusExpForPlayers, x['user_id']))
                        db.commit()
                        text = "Вы получили {}✨ и {}💰 за рейд башни".format(plusExpForPlayers, plusGoldForPlayer)
                    sql = "UPDATE users SET money = money + %s WHERE user_id = %s"
                    cursor.execute(sql, (plusGoldForPlayer, x['user_id']))
                    db.commit()
                    try:
                        bot.send_message(x['user_id'], text)
                    except:
                        pass
            sql = "UPDATE fraks SET fond = fond + goldAward WHERE name = %s"
            cursor.execute(sql, (z['name']))
            db.commit()
            needExp = z['lvl'] * 1000
            if z['exp'] + z['expAward'] >= needExp:
                plusExp = needExp - z['exp']
                newExp = (0 + (plusExp))
                sql = "UPDATE fraks SET lvl = lvl + 1 WHERE name = %s"
                cursor.execute(sql, (z['name']))
                db.commit()
                sql = "UPDATE fraks SET exp = %s WHERE name = %s"
                cursor.execute(sql, (newExp, z['name']))
                db.commit()
            sql = "UPDATE fraks SET exp = exp + expAward WHERE name = %s"
            cursor.execute(sql, (z['name']))
            sql = "UPDATE fraks SET goldAward = 0 WHERE name = %s"
            cursor.execute(sql, (z['name']))
            db.commit()
            sql = "UPDATE fraks SET expAward = 0 WHERE name = %s"
            cursor.execute(sql, (z['name']))
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (z['leader']))
            leader = cursor.fetchone()
            bot.send_message(leader['user_id'], "За этот рейд ваша группировка получила в фонд {}💰 и {}✨".format(z['goldAward'], z['expAward']))
        sql = "UPDATE users SET location = 'Хэвенбург' WHERE location = 'Первый этаж башни' OR location = 'Второй этаж башни' OR location = 'Третий этаж башни' OR location = 'Четвёртый этаж башни'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET position = 'Номер в отеле' WHERE location = 'Первый этаж башни' OR location = 'Второй этаж башни' OR location = 'Третий этаж башни' OR location = 'Четвёртый этаж башни'"
        cursor.execute(sql)
        db.commit()
a()