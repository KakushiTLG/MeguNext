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

def battleStart(player, enemy):
    battleid = ''
    symbols = 'qwertyuiopasdfghjklzxcvbnm'
    symbols += 'QWERTYUIOPASDFGHJKLZXCVBNM'
    symbols += '1234567890'
    for i in range(1,10):
        battleid += random.choice(symbols)
    text = "⚙️{}\n\n".format(battleid)
    db = on_db()
    with db.cursor() as cursor:
        sql = "INSERT INTO battle (idbattle, player, mob) VALUES (%s, %s, %s)"
        cursor.execute(sql, (battleid, player['id'], enemy['id']))
        db.commit()
        firstAtk = random.randint(1, 100)
        if firstAtk >= 50:
            sql = "SELECT * FROM inventory WHERE name = 'Свиток телепортации' AND idplayer = %s AND active = 1"
            cursor.execute(sql, (player['id']))
            tp = cursor.fetchone()
            #Player first atk
            text += "Вы атакуете первым."
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if tp:
                markup.add(InlineKeyboardButton('Телепортироваться в город', callback_data="battle_tp"))
            else:
                markup.add(InlineKeyboardButton('Отступить(Недоступно)', callback_data="battle_tpOff"))
            if player['item'] == 'Пистолет с ножом':
                markup.add(InlineKeyboardButton('Особый навык: Выстрел', callback_data="battle_shoot"))
            bot.send_message(player['user_id'], text, reply_markup=markup)
        else:
            armor = int(player['armor'] / 3)
            if enemy['atk'] < armor:
                armor = enemy['atk'] - 1
                playerNewHp = int(player['nowhp']) + armor - int(enemy['atk'])
            else:
                playerNewHp = int(player['nowhp']) + armor - int(enemy['atk'])
            if playerNewHp > 0:
                sql = "SELECT * FROM inventory WHERE name = 'Свиток телепортации' AND idplayer = %s AND active = 1"
                cursor.execute(sql, (player['id']))
                tp = cursor.fetchone()
                sql = "UPDATE users SET nowhp = %s WHERE user_id = %s"
                cursor.execute(sql, (playerNewHp, player['user_id']))
                db.commit()
                text += "{} атаковал вас первым. У вас осталось {}❤️(🛡{})".format(enemy['name'], playerNewHp, armor)
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if tp:
                    markup.add(InlineKeyboardButton('Телепортироваться в город', callback_data="battle_tp"))
                else:
                    markup.add(InlineKeyboardButton('Отступить(Недоступно)', callback_data="battle_tpOff"))
                bot.send_message(player['user_id'], text, reply_markup=markup)
            else:
                playerNewHp = 0
                loser = player['money'] * 0.5
                gorod = 'Город'
                text = "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(int(loser))
                sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE users SET position = 'Номер в отеле' WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE users SET battleStatus = 0 WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE monsters SET battleStatus = 0 WHERE id = %s"
                cursor.execute(sql, (enemy['id']))
                db.commit()
                sql = "UPDATE users SET eat = 100 WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE users SET energy = 100 WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                sql = "UPDATE users SET money = %s WHERE user_id = %s"
                cursor.execute(sql, (loser, player['user_id']))
                db.commit()
                sql = "UPDATE users SET nowhp = hp WHERE user_id = %s"
                cursor.execute(sql, (player['user_id']))
                db.commit()
                bot.send_message(player['user_id'], text)
        db.close()




def nav():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location != 'Город' AND progStatus = 1 AND battleStatus = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            if dict['location'] == 'Свалка':
                sql = "SELECT id FROM monsters ORDER BY id DESC"
                cursor.execute(sql)
                r = cursor.fetchone()
                randommob = random.randint(1, r['id'])
                sql = "SELECT * FROM monsters WHERE id = %s"
                cursor.execute(sql, (randommob))
                mob = cursor.fetchone()
                if mob and mob['battleStatus'] == 0:
                    text = "По пути вам встретился {}".format(mob['name'])
                    try:
                        sql = "UPDATE users SET battleStatus = 1 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET battleWith = %s WHERE user_id = %s"
                        cursor.execute(sql, (mob['id'], dict['user_id']))
                        db.commit()
                        sql = "UPDATE monsters SET battleWith = %s WHERE id = %s"
                        cursor.execute(sql, (dict['id'], mob['id']))
                        db.commit()
                        sql = "UPDATE monsters SET battleStatus = 1 WHERE id = %s"
                        cursor.execute(sql, (mob['id']))
                        db.commit()
                        bot.send_message(dict['user_id'], text)
                        player = dict
                        enemy = mob
                        battleStart(player, enemy)
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                else:
                    pass
            elif dict['location'] == 'Пустыня':
                progLoc = dict['progLoc']
                _prog = progLoc.split('|')
                newprog = int(_prog[1]) + 1
                newProgLoc = "{}|{}".format(_prog[0], newprog)
                sql = "SELECT size, next FROM locations WHERE name = %s"
                cursor.execute(sql, (dict['location']))
                loc = cursor.fetchone()
                sql = "SELECT * FROM inventory WHERE idplayer = %s AND name = 'Аптечка'"
                cursor.execute(sql, (dict['id']))
                checkdungeon = cursor.fetchone()
                if newprog == 13 and not checkdungeon:
                    text = "*ВНЕЗАПНО*\n\nК тебе подкрались из-за спины два человека, заломили руки и потащили с собой.\n\nНа твои вопросы отвечали лишь одной фразой: _«Заткнись, шизоид»_"
                    sql = "UPDATE `users` SET `location` = '🏥Логово сектантов' WHERE `user_id` = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    sql = "UPDATE `users` SET `progLoc` = '🏥Логово сектантов|0' WHERE `user_id` = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    try:
                        bot.send_message(dict['user_id'], text, parse_mode='markdown')
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                elif loc['size'] + 1 > newprog:
                    print("Pass")
                    sql = "SELECT * FROM monsters WHERE location = %s AND pos = %s AND battleStatus = 0"
                    cursor.execute(sql, (dict['location'], newprog))
                    mob = cursor.fetchone()
                    sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                    cursor.execute(sql, (newProgLoc, dict['user_id']))
                    db.commit()
                    if mob:
                        if mob['name'] == 'Шаи-Хулуд':
                            text = "Подходя к краю пустыни, ты вдруг услышал дикий рев из-под земли. Внезапно тебя накрыло стеной песка, сквозь который ничего не было видно, однако ощущение опасности тебя не покидало. Когда песок рассеялся, ты увидел до ужаса омерзительное чудовище, о котором сложены легенды в твоем городе. До того, как ты полностью его рассмотрел, ты понял - это 🔸Шаи-Хулуд🔸."
                            try:
                                photo = open('/home/kakushigoto/megu/media/shai.jpg', 'rb')
                                bot.send_photo(dict['user_id'], photo)
                            except:
                                import traceback
                                bot.send_message(702528084, str(traceback.format_exc()))
                                sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                                cursor.execute(sql, (dict['user_id']))
                                db.commit()
                        else:
                            text = "По пути вам встретился {}".format(mob['name'])
                        try:
                            sql = "UPDATE users SET battleStatus = 1 WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                            sql = "UPDATE users SET battleWith = %s WHERE user_id = %s"
                            cursor.execute(sql, (mob['id'], dict['user_id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleWith = %s WHERE id = %s"
                            cursor.execute(sql, (dict['id'], mob['id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleStatus = 1 WHERE id = %s"
                            cursor.execute(sql, (mob['id']))
                            db.commit()
                            bot.send_message(dict['user_id'], text)
                            sql = "SELECT * FROM users WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            player = cursor.fetchone()
                            enemy = mob
                            battleStart(player, enemy)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                    else:
                        pass
                else:
                    sql = "SELECT * FROM inventory WHERE idplayer = %s AND name = 'Большой город'"
                    cursor.execute(sql, (dict['id']))
                    a = cursor.fetchone()
                    if a:
                        sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        text = 'Эти дюны никогда не закон... Твоё нытье было прервано нагло появившимся под ногами КАМНЕМ, споткнувшись о который, ты полетел лицом вперёд и ощутил всю прелесть земли-матушки.'
                        text += '\n\nПосле тщательного унижения данной особи семейства камневых и всей его семьи, тебя смутило само присутствие земли и камней в пустыне.'
                        text += '\n\nОсмотревшись, ты осознал, что эти дюны всё-таки закончились и вот, спустя километры безжизненных  песков, ты узрел цивилизацию — новый город, кажется он даже круче того захолустья, из которого ты прибыл.'
                        text += '\n\nТочно, это ведь Хэвенбург...'
                        bot.send_message(dict['user_id'], text)
                    else:
                        text = 'Эти дюны никогда не закон... Твоё нытье было прервано нагло появившимся под ногами КАМНЕМ, споткнувшись о который, ты полетел лицом вперёд и ощутил всю прелесть земли-матушки.'
                        text += '\n\nПосле тщательного унижения данной особи семейства камневых и всей его семьи, тебя смутило само присутствие земли и камней в пустыне.'
                        text += '\n\nОсмотревшись, ты осознал, что эти дюны всё-таки закончились и вот, спустя километры безжизненных  песков, ты узрел цивилизацию — новый город, кажется он даже круче того захолустья, из которого ты прибыл.'
                        text += '\n\nПроверим, не попался ли ты на пранк очередного миража...'
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('К городу', callback_data="startstartBigCity"))
                        bot.send_message(dict['user_id'], text, reply_markup=markup)
                        sql = "UPDATE users SET progLoc = 'Большой город|0' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET location = 'Большой город' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                    bot.send_message(-1001317123616, "Игрок {} прошёл локацию Пустыня".format(dict['username']))

###################################################################################################################
            elif dict['location'] == '🏥Логово сектантов':
                progLoc = dict['progLoc']
                _prog = progLoc.split('|')
                newprog = int(_prog[1]) + 1
                newProgLoc = "{}|{}".format(_prog[0], newprog)
                sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                cursor.execute(sql, (newProgLoc, dict['user_id']))
                db.commit()
                if newprog == 1:
                    text = "_Тебя бросили в коридоре, наглухо захлопнув дверь выхода. Сказали никуда не уходить._ \n\nТы ушёл искать иной путь отступления..."
                    try:
                        bot.send_message(dict['user_id'], text, parse_mode='markdown')
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                elif newprog <= 6:
                    sql = "SELECT * FROM monsters WHERE location = '🏥Логово сектантов' ORDER BY RAND() Limit 1"
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    if res['battleStatus'] == 0:
                        text = "По пути вам встретился {}".format(res['name'])
                        try:
                            sql = "UPDATE users SET battleStatus = 1 WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                            sql = "UPDATE users SET battleWith = %s WHERE user_id = %s"
                            cursor.execute(sql, (res['id'], dict['user_id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleWith = %s WHERE id = %s"
                            cursor.execute(sql, (dict['id'], res['id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleStatus = 1 WHERE id = %s"
                            cursor.execute(sql, (res['id']))
                            db.commit()
                            bot.send_message(dict['user_id'], text)
                            player = dict
                            enemy = res
                            battleStart(player, enemy)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                elif newprog == 7:
                    sql = "SELECT * FROM monsters WHERE location = '🏥Логово сектантов' AND name = ' 🚑Главврач'"
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    if res['battleStatus'] == 0:
                        text = "По пути вам встретился {}".format(res['name'])
                        try:
                            sql = "UPDATE users SET battleStatus = 1 WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                            sql = "UPDATE users SET battleWith = %s WHERE user_id = %s"
                            cursor.execute(sql, (res['id'], dict['user_id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleWith = %s WHERE id = %s"
                            cursor.execute(sql, (dict['id'], res['id']))
                            db.commit()
                            sql = "UPDATE monsters SET battleStatus = 1 WHERE id = %s"
                            cursor.execute(sql, (res['id']))
                            db.commit()
                            bot.send_message(dict['user_id'], text)
                            player = dict
                            enemy = res
                            battleStart(player, enemy)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                elif newprog == 8:
                    text = "_Украв бейджик врача и его ключи, ты горделивой походкой, зыркая на встречных сектантов, покинул данное заведение_"
                    sql = "UPDATE users SET location = 'Пустыня' WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    sql = "UPDATE users SET progLoc = 'Пустыня|13' WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    try:
                        bot.send_message(dict['user_id'], text, parse_mode='markdown')
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
#######################################################################################################
#                    else:
#                        newProgLoc = "{}|0".format(loc['next'])
#                        sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
#                        cursor.execute(sql, (newProgLoc, dict['user_id']))
#                        db.commit()
#                        sql = "UPDATE users SET location = %s WHERE user_id = %s"
#                        cursor.execute(sql, (loc['next'], dict['user_id']))
#                        db.commit()
#                        try:
#                            bot.send_message(dict['user_id'], "Вы успешно исследовали локацию {} и перешли в {}".format(dict['location'], loc['next']))
#                        except:
#                            sql = "UPDATE users SET location = 'Город' WHERE user_id = %s"
#                            cursor.execute(sql, (dict['user_id']))
#                            db.commit()
        db.close()


try:
    nav()
except:
    import traceback
    bot.send_message(702528084, str(traceback.format_exc()))
