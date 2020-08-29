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
    for i in range(1,15):
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
                markup.add(InlineKeyboardButton('Телепортироваться в Хэвенбург', callback_data="battle_tp"))
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
                    markup.add(InlineKeyboardButton('Телепортироваться в Хэвенбург', callback_data="battle_tp"))
                else:
                    markup.add(InlineKeyboardButton('Отступить(Недоступно)', callback_data="battle_tpOff"))
                bot.send_message(player['user_id'], text, reply_markup=markup)
            else:
                playerNewHp = 0
                loser = player['money'] * 0.5
                gorod = 'Хэвенбург'
                text = "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(int(loser))
                sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
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


dungeons = ['Лесная гробница']
emojis = {'Лесная гробница': '🕯Лесная гробница'}
def nav():
    global dungeons
    global emojis
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE location != 'Хэвенбург' AND progStatus = 1 AND battleStatus = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
        for dict in result:
            if dict['location'] == 'Большая свалка':
                _random = random.randint(1, 100)
                nowProgLoc = dict['progLoc']
                _pl = nowProgLoc.split('|')
                num = _pl[1]
                newnum = int(num) + 1
                newProgLoc = "Большая свалка|{}".format(newnum)
                sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                cursor.execute(sql, (newProgLoc, dict['user_id']))
                db.commit()
                if _random >= 25:
                    sql = "SELECT id FROM monsters ORDER BY id DESC"
                    cursor.execute(sql)
                    r = cursor.fetchone()
                    randommob = random.randint(1, r['id'])
                    sql = "SELECT * FROM monsters WHERE id = %s"
                    cursor.execute(sql, (randommob))
                    mob = cursor.fetchone()
                    if mob and mob['battleStatus'] == 0:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Большая свалка: К-{}\n\nНа тебя вылез {}\nОсмотреться - /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum, mob['name'])
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
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                    else:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Большая свалка: К-{}\n\nОсмотреться вокруг /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum)
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        try:
                            markup = InlineKeyboardMarkup()
                            markup.row_width = 2
                            markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                            bot.send_message(dict['user_id'], text, reply_markup=markup)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                else:
                    text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Большая свалка: К-{}\n\nОсмотреться вокруг /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum)
                    sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    try:
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                        bot.send_message(dict['user_id'], text, reply_markup=markup)
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
            elif dict['location'] == 'Случайный лес':
                _random = random.randint(1, 100)
                nowProgLoc = dict['progLoc']
                _pl = nowProgLoc.split('|')
                num = _pl[1]
                newnum = int(num) + 1
                newProgLoc = "Случайный лес|{}".format(newnum)
                sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                cursor.execute(sql, (newProgLoc, dict['user_id']))
                db.commit()
                print(_random)
                if _random >= 20:
                    progLoc = dict['progLoc']
                    _prog = progLoc.split('|')
                    newprog = int(_prog[1]) + 1
                    newProgLoc = "{}|{}".format(_prog[0], newprog)
                    sql = "SELECT size, next FROM locations WHERE name = %s"
                    cursor.execute(sql, (dict['location']))
                    loc = cursor.fetchone()
                    if loc['size'] + 1 > newprog:
                        print("Pass")
                        sql = "SELECT * FROM monsters WHERE location = %s AND pos = %s AND battleStatus = 0"
                        cursor.execute(sql, (dict['location'], newprog))
                        mob = cursor.fetchone()
                        sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                        cursor.execute(sql, (newProgLoc, dict['user_id']))
                        db.commit()
                        if not mob:
                            if newnum == 35:
                                try:
                                    text = 'Внезапно тропа разделяется надвое: одна все так же ведёт прямо, но другая становится мрачнее и уходит в сторону.\nДальше лишь укрытый грозовыми облаками и мертвыми деревьями путь невесть куда.\n_Кажется, здесь начинается путь к небезысвестной «Лесной гробнице», пик которой виднеется где-то вдалеке средь гнилых ветвей да разящих молний._'
                                    markup = InlineKeyboardMarkup()
                                    markup.row_width = 2
                                    markup.add(InlineKeyboardButton('К 🕯️Лесной гробнице', callback_data="dunjgo_grob"))
                                    markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                                    bot.send_message(dict['user_id'], text, reply_markup=markup, parse_mode='markdown')
                                except:
                                    import traceback
                                    bot.send_message(702528084, str(traceback.format_exc()))
                                    sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                    cursor.execute(sql, (dict['user_id']))
                                    db.commit()
                            else:
                                try:
                                    text = "Всматриваясь вдаль, ты не видишь никаких следов жизни..."
                                    bot.send_message(dict['user_id'], text)
                                except:
                                    import traceback
                                    bot.send_message(702528084, str(traceback.format_exc()))
                                    sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                    cursor.execute(sql, (dict['user_id']))
                                    db.commit()
                        if mob and mob['battleStatus'] == 0:
                            if mob['name'] == ' 🧞‍♂️Солмир🧞‍♂️':
                                newhp = int(dict['nowhp'] / 2)
                                dict['nowhp'] = newhp
                                sql = "UPDATE users SET nowhp = %s WHERE user_id = %s"
                                cursor.execute(sql, (newhp, dict['user_id']))
                                db.commit()
                                text = "По пути вам встретился 🧞‍♂Солмир🧞‍♂\nОн застал вас врасплох своей способностью цепной молнии и оставил вам {}❤️".format(newhp)
                                try:
                                    photo = open('/home/kakushigoto/megu/media/solmir.jpg', 'rb')
                                    audio = open('/home/kakushigoto/megu/media/Battle_Theme_3_Heroes.mp3', 'rb')
                                    bot.send_photo(dict['user_id'], photo, text)
                                    bot.send_audio(dict['user_id'], audio)
                                    text = "Битва начинается!"
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
                                text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀Случайный лес: К-{}\n\nНа тебя вылез {}\nОсмотреться /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum, mob['name'])
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
                                    sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                    cursor.execute(sql, (dict['user_id']))
                                    db.commit()
                        else:
                            text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀Случайный лес: К-{}\n\nОсмотреться вокруг /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum)
                            sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                            try:
                                markup = InlineKeyboardMarkup()
                                markup.row_width = 2
                                markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                                if newnum == 35:
                                    text += '\n\n\nВнезапно тропа разделяется надвое: одна все так же ведёт прямо, но другая становится мрачнее и уходит в сторону.\nДальше лишь укрытый грозовыми облаками и мертвыми деревьями путь невесть куда.\nКажется, здесь начинается путь к небезысвестной «Лесной гробнице», пик которой виднеется где-то вдалеке средь гнилых ветвей да разящих молний'
                                    markup = InlineKeyboardMarkup()
                                    markup.row_width = 2
                                    markup.add(InlineKeyboardButton('К 🕯️Лесной гробнице', callback_data="dunjgo_grob"))
                                bot.send_message(dict['user_id'], text, reply_markup=markup)
                            except:
                                import traceback
                                bot.send_message(702528084, str(traceback.format_exc()))
                                sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                cursor.execute(sql, (dict['user_id']))
                                db.commit()
                else:
                    text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀Случайный лес: К-{}\n\nОсмотреться вокруг /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum)
                    sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    try:
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                        if newnum == 35:
                            text += '\n\n\nВнезапно тропа разделяется надвое: одна все так же ведёт прямо, но другая становится мрачнее и уходит в сторону.\nДальше лишь укрытый грозовыми облаками и мертвыми деревьями путь невесть куда.\nКажется, здесь начинается путь к небезысвестной «Лесной гробнице», пик которой виднеется где-то вдалеке средь гнилых ветвей да разящих молний'
                            markup.add(InlineKeyboardButton('К 🕯️Лесной гробнице', callback_data="dunjgo_grob"))
                        bot.send_message(dict['user_id'], text, reply_markup=markup)
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
            if dict['location'] == "Тропа к башне":
                nowProgLoc = dict['progLoc']
                _pl = nowProgLoc.split('|')
                num = _pl[1]
                newnum = int(num) + 1
                newProgLoc = "Тропа к башне|{}".format(newnum)
                sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                cursor.execute(sql, (newProgLoc, dict['user_id']))
                db.commit()
                sql = "SELECT size, next FROM locations WHERE name = %s"
                cursor.execute(sql, (dict['location']))
                loc = cursor.fetchone()
                if loc['size'] + 1 > newnum:
                    print("Pass nav tower")
                    sql = "SELECT * FROM monsters WHERE location = %s AND pos = %s AND battleStatus = 0"
                    cursor.execute(sql, (dict['location'], newnum))
                    mob = cursor.fetchone()
                    sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                    cursor.execute(sql, (newProgLoc, dict['user_id']))
                    db.commit()
                    if mob and mob['battleStatus'] == 0:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀Тропа к башне: К-{}\n\nНа тебя вылез {}\nОсмотреться /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum, mob['name'])
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
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                    else:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀Тропа к башне: К-{}\n\nОсмотреться вокруг /watch_around".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], newnum)
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        try:
                            markup = InlineKeyboardMarkup()
                            markup.row_width = 2
                            markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                            bot.send_message(dict['user_id'], text, reply_markup=markup)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                else:
                    sql = "UPDATE users SET location = 'Башня' WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    bot.send_message(dict['user_id'], towerText)
            elif dict['location'] in dungeons:
                nowProgLoc = dict['progLoc']
                _pl = nowProgLoc.split('|')
                num = _pl[1]
                newnum = int(num) + 1
                newProgLoc = "{}|{}".format(dict['location'], newnum)
                sql = "UPDATE users SET progLoc = %s WHERE user_id = %s"
                cursor.execute(sql, (newProgLoc, dict['user_id']))
                db.commit()
                sql = "SELECT size, next FROM locations WHERE name = %s"
                cursor.execute(sql, (dict['location']))
                loc = cursor.fetchone()
                if loc['size'] + 1 > newnum:
                    sql = "SELECT * FROM monsters WHERE location = %s AND pos = %s AND battleStatus = 0"
                    cursor.execute(sql, (dict['location'], newnum))
                    mob = cursor.fetchone()
                    rand = random.randint(1, 10)
                    if rand >= 2:
                        if mob and mob['battleStatus'] == 0:
                            text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n{}\n\nНа тебя вылез {}".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], emojis[dict['location']], mob['name'])
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
                                sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                cursor.execute(sql, (dict['user_id']))
                                db.commit()
                        else:
                            text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n{}\n\nВокруг пока что тихо, никого не видать...".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], emojis[dict['location']], mob['name'])
                            sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                            try:
                                markup = InlineKeyboardMarkup()
                                markup.row_width = 2
                                markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                                bot.send_message(dict['user_id'], text, reply_markup=markup)
                            except:
                                import traceback
                                bot.send_message(702528084, str(traceback.format_exc()))
                                sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                                cursor.execute(sql, (dict['user_id']))
                                db.commit()
                    else:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🌀{}\n\nТы наткнулся на развилку. Куда пойдёшь?".format(dict['nowhp'], dict['hp'], dict['energy'], dict['eat'], dict['location'], mob['name'])
                        sql = "UPDATE users SET progStatus = 0 WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
                        try:
                            markup = InlineKeyboardMarkup()
                            markup.row_width = 2
                            markup.add(InlineKeyboardButton('Идти прямо', callback_data="navgo"))
                            markup.add(InlineKeyboardButton('Повернуть направо', callback_data="navgo"))
                            markup.add(InlineKeyboardButton('Повернуть налево', callback_data="navgo"))
                            bot.send_message(dict['user_id'], text, reply_markup=markup)
                        except:
                            import traceback
                            bot.send_message(702528084, str(traceback.format_exc()))
                            sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                            cursor.execute(sql, (dict['user_id']))
                            db.commit()
                else:
                    sql = "UPDATE users SET progLoc = 'Случайный лес|36' WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    db.commit()
                    sql = "UPDATE users SET progStatus = 1 WHERE user_id = %s"
                    cursor.execute(sql, (dict['user_id']))
                    try:
                        text = "Ты вышел к лесу обратно..."
                        bot.send_message(dict['user_id'], text, reply_markup=markup)
                    except:
                        import traceback
                        bot.send_message(702528084, str(traceback.format_exc()))
                        sql = "UPDATE users SET location = 'Хэвенбург' WHERE user_id = %s"
                        cursor.execute(sql, (dict['user_id']))
                        db.commit()
        db.close()



towerText = """Башня — важнейшая достопримечательность в радиусе нескольких сотен километров и главный источник шуток про член.

Необъятная и бескрайняя — она стоит здесь с древних времён, странная, непонятная и... серая. Мнения людей расходятся, как только речь заходит о создателе сей древней конструкции.

Кто-то считает, что это проделки ящеролюдов во главе с неким Биллусом Гейцем, другие склоняются к теории об инопланетянах или даже высших силах, узрить которые мы не в силах.

Ну а пока никто не выяснил зачем и откуда она тут взялась, для простых людей это просто крайне опасный каменный стояк до небес. Почему опасный? Загляни внутрь, когда башня распахнёт свои врата для тех смертников, которые сюда постоянно ходят."""



try:
    nav()
except:
    import traceback
    bot.send_message(702528084, str(traceback.format_exc()))
