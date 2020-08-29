import pymysql
import telebot
import os
import random
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

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

def PvEStart(player, enemy):
    playerArmor = int(player['armor'] / 3)
    player = {'username': player['username'], 'armor': playerArmor, 'atk': player['atk'], 'hp': player['nowhp'], 'user_id': player['user_id'], 'frak': player['frak']}
    enemy = {'username': enemy['name'], 'atk': enemy['atk'], 'hp': enemy['nowhp'], 'id': enemy['id']}
    FATK = random.randint(0, 100)
    bot.send_message(player['user_id'], "👤{} VS 👤{}\n\n\n".format(player['username'], enemy['username']))
    minPlayerAtk = int(player['atk'] * 0.9)
    maxPlayerAtk = int(player['atk'] * 1.1)
    minEnemyAtk = int(enemy['atk'] * 0.9)
    maxEnemyAtk = int(enemy['atk'] * 1.1)
    if FATK >= 50:
        pAtk = random.randint(minPlayerAtk, maxPlayerAtk)
        playerAtk = pAtk
        step = 1
        enemy['hp'] = enemy['hp'] - playerAtk
        textPlayer = "👤{} нанес удар {}💥".format(player['username'], pAtk)
    else:
        eAtk = random.randint(minEnemyAtk, maxEnemyAtk)
        if eAtk <= playerArmor:
            pArmor = eAtk - 1        
        else:
            pArmor = playerArmor
        enemyAtk = eAtk - pArmor
        step = 2
        player['hp'] = player['hp'] - enemyAtk
        textPlayer = "👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], eAtk, pArmor)
    while player['hp'] > 0 and enemy['hp'] > 0:
        step += 1
        pAtk = random.randint(minPlayerAtk, maxPlayerAtk) 
        playerAtk = pAtk
        eAtk = random.randint(minEnemyAtk, maxEnemyAtk) 
        if eAtk <= playerArmor:
            pArmor = eAtk - 1        
        else:
            pArmor = playerArmor
        enemyAtk = eAtk - pArmor
        if step/2 == step//2: #Атака enemy
            player['hp'] = player['hp'] - enemyAtk
            if player['hp'] < 0:
                player['hp'] = 0
            textPlayer += "\n👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], str(eAtk), pArmor)
        else: #Атака player
            enemy['hp'] = enemy['hp'] - playerAtk
            if enemy['hp'] < 0:
                enemy['hp'] = 0
            textPlayer += "\n👤{} нанес удар {}💥".format(player['username'], str(pAtk))
    if player['hp'] <= 0:
        textPlayer += "\n\n_Тебя знатно потрепали, но не до смерти.Твоё тело оттащили в город._"
        db = on_db()
        with db.cursor() as cursor:
            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
            cursor.execute(sql, (player['user_id']))
            db.commit()
            sql = "UPDATE users SET position = 'Номер в отеле' WHERE user_id = %s"
            cursor.execute(sql, (player['user_id']))
            db.commit()
            sql = "UPDATE users SET nowhp = hp WHERE user_id = %s"
            cursor.execute(sql, (player['user_id']))
            db.commit()
            sql = "UPDATE users SET progLoc = 'Хэвенбург|0' WHERE user_id = %s"
            cursor.execute(sql, (player['user_id']))
            db.commit()
            sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
            cursor.execute(sql, (player['user_id']))
            db.commit()
        db.close()
    else:
        db = on_db()
        with db.cursor() as cursor:
            sql = "SELECT * FROM monsters WHERE id = %s"
            cursor.execute(sql, (enemy['id']))
            res = cursor.fetchone()
            sql = "UPDATE fraks SET expAward = expAward + %s WHERE name = %s"
            cursor.execute(sql, (res['maxexp'], player['frak']))
            db.commit()
            sql = "UPDATE fraks SET goldAward = goldAward + %s WHERE name = %s"
            cursor.execute(sql, (res['maxgold'], player['frak']))
            db.commit()
            sql = "UPDATE users SET nowhp = %s WHERE user_id = %s"
            cursor.execute(sql, (player['hp'], player['user_id']))
            db.commit()
        db.close()
        textPlayer += "\n\n_Ты вышел победителем из этой схватки и снова кинулся в гущу сражений_"
    bot.send_message(player['user_id'], textPlayer, parse_mode='markdown')


def a():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location = 'Первый этаж башни' OR location = 'Второй этаж башни' OR location = 'Третий этаж башни' OR location = 'Четвёртый этаж башни' OR location = 'Пятый этаж башни' OR location = 'Шестой этаж башни' OR location = 'Седьмой этаж башни'"
        cursor.execute(sql)
        result = cursor.fetchall()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for z in result:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            nowProgLoc = z['progLoc']
            _pl = nowProgLoc.split('|')
            num = int(_pl[1])
            if z['location'] == 'Первый этаж башни' and num >= 5 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                markup.add(InlineKeyboardButton('Идти на второй этаж башни', callback_data="tower_2"))
                markup.add(InlineKeyboardButton('Возвращаться в город', callback_data="battle_tp"))
                bot.send_message(z['user_id'], "Вы дошли до конца этажа. \n\nВы можете идти со своей группировкой на второй этаж, но если вас отзывают в город - вам следует телепортироваться.", reply_markup=markup)
            elif z['location'] == 'Второй этаж башни' and num >= 7 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                markup.add(InlineKeyboardButton('Идти на третий этаж башни', callback_data="tower_3"))
                markup.add(InlineKeyboardButton('Возвращаться в город', callback_data="battle_tp"))
                bot.send_message(z['user_id'], "Вы дошли до конца этажа. \n\nВы можете идти со своей группировкой на третий этаж, но если вас отзывают в город - вам следует телепортироваться.", reply_markup=markup)
            elif z['location'] == 'Третий этаж башни' and num >= 9 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                markup.add(InlineKeyboardButton('Идти на четвёртый этаж башни', callback_data="tower_4"))
                markup.add(InlineKeyboardButton('Возвращаться в город', callback_data="battle_tp"))
                bot.send_message(z['user_id'], "Вы дошли до конца этажа. \n\nВы можете идти со своей группировкой на четвёртый этаж, но если вас отзывают в город - вам следует телепортироваться.", reply_markup=markup)
            elif z['location'] == 'Четвёртый этаж башни' and num >= 11 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                bot.send_message(z['user_id'], "Вы дошли до конца этажа.")
            elif z['location'] == 'Пятый этаж башни' and num >= 13 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
            elif z['location'] == 'Шестой этаж башни' and num >= 15 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                bot.send_message(z['user_id'], "Вы дошли до конца этажа")
            elif z['location'] == 'Седьмой этаж башни' and num >= 20 and z['progStatus'] == 1:
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (z['user_id']))
                db.commit()
                bot.send_message(z['user_id'], "Вы дошли до конца этажа")
            else:
                if z['progStatus'] == 1:
                    newnum = int(num) + 1
                    newProgLoc = "{}|{}".format(_pl[0], newnum)
                    sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                    cursor.execute(sql, (newProgLoc, z['user_id']))
                    db.commit()
                    sql = "SELECT * FROM monsters WHERE location = %s AND pos = %s"
                    cursor.execute(sql, (z['location'], newnum))
                    mob = cursor.fetchone()
                    text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Башня\n\nНа тебя вылез {}".format(z['nowhp'], z['hp'], z['energy'], z['eat'], mob['name'])
                    PvEStart(z, mob)
    db.close()
a()