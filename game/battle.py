import time
import random
"""@bot.message_handler(commands=['atk'])
def atk(m): 
    do = 'atk'
    if do == 'atk':
        result = db.Users.get(user_id=m.from_user.id)
        idp = result
        location = result.location
        pName = result.username
        armor = int(result.armor / 3)
        if result.battleStatus == 1:
            pass
        else:
            return
        er = db.Monsters.get(id=result.battleWith)
        if (result.nowhp > 0) and (er.nowhp > 0):
            item = result.item
            _itemAtk = result.lvl / 100
            if result.item == "Пистолет с ножом":
                Atk = int(result.atk * 1.3)
                playerAtk = int(Atk)
            elif result.item == "Копьё":
                Atk = int(result.atk * 1.4)
                playerAtk = int(Atk)
            else:
                itemAtk = 1 + _itemAtk
                Atk = result.atk * itemAtk
                playerAtk = int(Atk)
            enemyNewHp = int(er.nowhp) - int(playerAtk)
            er.nowhp = enemyNewHp
            er.save()
            if enemyNewHp > 0:
                if er.atk < armor:
                    armor = er.atk
                    playerNewHp = int(result.nowhp) + armor - int(er.atk)
                else:
                    playerNewHp = int(result.nowhp) + armor - int(er.atk)
                if playerNewHp <= 0:
                    money = int(result.money)
                    loser = int(money * 0.5)
                    gorod = 'Город'
                    text = ""
                    text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                    result.money = loser
                    result.location = gorod
                    result.battleStatus = 0
                    er.battleStatus = 0
                    er.nowhp = er.hp
                    result.energy = 100
                    result.eat = 100
                    result.progStatus = 1
                    result.save()
                    er.save()
                    gg = bot.reply_to(m, text)
                    return
                result.nowhp = playerNewHp
                result.save()
                text = m.text
                text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(result.username), str(er.name), str(int(playerAtk)), str(er.name), str(result.username), str(er.atk), str(armor), str(playerNewHp))
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if result.item == "Меч": #Начинается скрипт скиллов
                    fullHpMob = int(er.hp)
                    needHpToSkill = fullHpMob * 0.1
                    if enemyNewHp <= needHpToSkill:
                        markup.add(InlineKeyboardButton('Особый навык: Казнь', callback_data="battle_kazn"))
                    else:
                        pass
                elif result.item == "Пистолет с ножом":
                    randomShot = random.randint(0, 100)
                    if randomShot <= 20:
                        markup.add(InlineKeyboardButton('Особый навык: Выстрел', callback_data="battle_shoot"))
                elif result.item == "Копьё":
                    randomAtk = random.randint(0, 100)
                    if randomAtk <= 25:
                        markup.add(InlineKeyboardButton('Особый навык: Серия ударов', callback_data="battle_seriya"))
                elif result.item == "Катана":
                    randomKill = random.randint(0, 100)
                    if randomKill <= 15:
                        markup.add(InlineKeyboardButton('Особый навык: Рубящий удар', callback_data="battle_oneshot"))
                pId = result.id
                pIdName = "Свиток телепортации"
                o = db.Inventory.get(active=1, name=pIdName, idplayer=pId)
                if o:
                    markup.add(InlineKeyboardButton('Телепортация в город', callback_data="battle_tp"))
                else:
                    markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
                gg = bot.reply_to(m, text, reply_markup=markup)
                return
            else:
                gold, exp, sometext = db.winner(idp, location)
                text = ""
                text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
                result.battleStatus = 0
                result.progStatus = 1
                er.battleStatus = 0
                er.nowhp = er.hp
                result.save()
                er.save()
            gg = bot.reply_to(m, text)
            return
        else:
            text = ""
            if (int(result.nowhp) <= 0):
                money = int(result.money)
                loser = money * 0.5
                gorod = 'Город'
                text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                result.money = loser
                result.location = gorod
                result.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                result.progStatus = 1
                result.eat = 100
                result.energy = 100
                result.nowhp = result.hp
                er.save()
                result.save()
                gg = bot.reply_to(m, text)
            elif (int(er.nowhp) <= 0):
                gold, exp, sometext = db.winner(idp, location)
                text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
                result.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                result.progStatus = 1
                er.save()
                result.save()
                gg = bot.reply_to(m, text)

@bot.message_handler(commands=['tp'])
def tp(m): 
    do = 'tp'
    if do == 'tp':
        res = db.Users.get(user_id=m.from_user.id)
        pId = res.id
        pIdName = "Свиток телепортации"
        o = db.Inventory.get(active=1, name=pIdName, idplayer=pId)
        if o:
            pass
        else:
            er = db.Monsters.get(battleWith=res.id)
            playerNewHp = int(res.nowhp) - int(er.atk)
            text = ""
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
            if playerNewHp < 1:
                money = int(res.money)
                loser = int(money * 0.5)
                gorod = 'Город'
                text += "Пытаясь вытащить 📜Свиток телепортации, враг всё же смог нанести тебе смертельный удар. За возрождение в городе снято {}💰".format(str(loser))
                res.money = loser
                res.location = gorod
                res.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                res.nowhp = res.hp
                res.energy = 100
                res.eat = 100
                res.progStatus = 1
                res.save()
                er.save()
                gg = bot.reply_to(m, text, reply_markup=markup)
                return
            else:
                text += "Пытаясь вытащить 📜Свиток телепортации, враг всё же смог тебя зацепить, однако свитка ты не нашёл. Битва продолжается. \nУ вас осталось {}❤️\n----------".format(str(playerNewHp))
                res.nowhp = playerNewHp
                res.save()
                return
        res.battleStatus = 0
        er.battleStatus = 0
        res.save()
        er.save()
        newLoc = "Город"
        newPos = "Площадь"
        res.location = newLoc
        res.position = newPos
        ores = db.Inventory.get(active=1, name=pIdName, idplayer=res.id)
        ores.active = 0
        ores.save()
        text = ""
        text += "\nВы успешно телепортировались в город."
        gg = bot.reply_to(m, text)

"""

buzyusrs = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('battle_'))
def battlestart(call): 
    global buzyusrs
    try:
        if buzyusrs[call.message.chat.id]:
            if buzyusrs[call.message.chat.id] > time.time():
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Анти-флуд. Попробуй через секунду")                
                return
            else:
                buzyusrs[call.message.chat.id] = int(time.time()) + 2
    except:
        buzyusrs[call.message.chat.id] = int(time.time()) + 2
    btl = call.data.split('_')
    do = btl[1]
    result = db.Users.get(user_id=call.from_user.id)
    er = db.Monsters.get(id=result.battleWith)
    if result.battleStatus == 1:
        pass
    elif result.location == 'Первый этаж башни' or result.location == 'Второй этаж башни' or result.location == 'Третий этаж башни' or result.location == 'Четвёртый этаж башни':
        success = db.addItem('Свиток телепортации', result)
        if success:
            pass
        else:
            return
    else:
        gg = bot.edit_message_text("Битва с мобом окончена", call.message.chat.id, call.message.message_id)
        return
    if do == 'tp':
        er = db.Monsters.get(id=result.battleWith)
        q = result
        pIdName = "Свиток телепортации"
        o = db.Inventory.get(active=1, name=pIdName, idplayer=q.id)
        if o:
            pass
        else:
            res = result
            er = db.Monsters.get(battleWith=res.id)
            playerNewHp = int(res.nowhp) - int(er.atk)
            text = str(call.message.text)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
            if playerNewHp < 1:
                money = int(res.money)
                loser = int(money * 0.5)
                checkgorod = db.Inventory.get(idplayer=result.id, name='Большой город')
                if checkgorod:
                    result.location = 'Хэвенбург'
                else:
                    result.location = 'Город'
                text += "Пытаясь вытащить 📜Свиток телепортации, враг всё же смог нанести тебе смертельный удар. За возрождение в городе снято {}💰".format(str(loser))
                result.money = loser
                result.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                result.nowhp = res.hp
                result.energy = 100
                result.eat = 100
                result.progStatus = 1
                result.save()
                er.save()
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
            else:
                text += "\nПытаясь вытащить 📜Свиток телепортации, враг всё же смог тебя зацепить, однако свитка ты не нашёл. Битва продолжается. \nУ вас осталось {}❤️\n----------".format(str(playerNewHp))
                res.nowhp = playerNewHp
                res.save()
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
                return
        result.battleStatus = 0
        er.battleStatus = 0
        checkgorod = db.Inventory.get(idplayer=result.id, name='Большой город')
        if checkgorod:
            result.location = 'Хэвенбург'
        else:
            result.location = 'Город'
        result.position = 'Площадь'
        ores = db.Inventory.get(active=1, name=pIdName, idplayer=result.id)
        ores.active = 0
        result.save()
        er.save()
        ores.save()
        text = str(call.message.text)
        text += "\nВы успешно телепортировались в город."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif do == 'tpOff':
        return
    elif do == 'atk':
        result = db.Users.get(user_id=call.from_user.id)
        idp = result
        location = result.location
        pName = result.username
        armor = int(result.armor / 3)
        er = db.Monsters.get(id=result.battleWith)
        if (result.nowhp > 0) and (er.nowhp > 0):
            _itemAtk = result.lvl / 100
            if result.item == "Пистолет с ножом":
                playerAtk = int(result.atk * 1.3)
            elif result.item == "Копьё":
                playerAtk = int(result.atk * 1.4)
            else:
                itemAtk = 1 + _itemAtk
                playerAtk = int(result.atk * itemAtk)
            enemyNewHp = int(er.nowhp) - int(playerAtk)
            er.nowhp = enemyNewHp
            er.save()
            if enemyNewHp > 0:
                if er.atk < armor:
                    armor = er.atk - 1
                elif er.atk == armor:
                    armor = er.atk - 1
                playerNewHp = int(result.nowhp) + armor - int(er.atk)
                if playerNewHp <= 0:
                    money = int(result.money)
                    loser = int(money * 0.5)
                    checkgorod = db.Inventory.get(idplayer=result.id, name='Большой город')
                    if checkgorod:
                        result.location = 'Хэвенбург'
                    else:
                        result.location = 'Город'
                    text = str(call.message.text)
                    text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                    result.money = loser
                    result.battleStatus = 0
                    er.battleStatus = 0
                    er.nowhp = er.hp
                    result.nowhp = result.hp
                    result.eat = 100
                    result.energy = 100
                    result.progStatus = 1
                    er.save()
                    result.save()
                    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                    return
                result.nowhp = playerNewHp
                result.save()
                text = call.message.text
                text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(er.atk), str(armor), str(playerNewHp))
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                randomSkill = random.randint(0, 100)
                if result.item == "Меч": #Начинается скрипт скиллов
                    fullHpMob = int(er.hp)
                    needHpToSkill = fullHpMob * 0.13
                    if enemyNewHp <= needHpToSkill:
                        markup.add(InlineKeyboardButton('Особый навык: Казнь', callback_data="battle_kazn"))
                    else:
                        pass
                elif result.item == "Пистолет с ножом":
                    if randomSkill <= 20:
                        markup.add(InlineKeyboardButton('Особый навык: Выстрел', callback_data="battle_shoot"))
                elif result.item == "Копьё":
                    if randomSkill <= 20:
                        markup.add(InlineKeyboardButton('Особый навык: Серия ударов', callback_data="battle_seriya"))
                elif result.item == "Катана":
                    if randomSkill <= 25:
                        markup.add(InlineKeyboardButton('Особый навык: Рубящий удар', callback_data="battle_oneshot"))
                pId = result.id
                pIdName = "Свиток телепортации"
                o = db.Inventory.get(active=1, name=pIdName, idplayer=pId)
                if o:
                    markup.add(InlineKeyboardButton('Телепортация в город', callback_data="battle_tp"))
                else:
                    markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
                return
            else:
                gold, exp, sometext = db.winner(idp, location)
                text = str(call.message.text)
                text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
                result.battleStatus = 0
                result.progStatus = 1
                er.battleStatus = 0
                er.nowhp = er.hp
                result.save()
                er.save()
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
        else:
            if (int(result.nowhp) <= 0):
                money = int(result.money)
                loser = money * 0.5
                checkgorod = db.Inventory.get(idplayer=result.id, name='Большой город')
                if checkgorod:
                    result.location = 'Хэвенбург'
                else:
                    result.location = 'Город'
                text = str(call.message.text)
                text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                result.money = loser
                result.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                result.progStatus = 1
                result.eat = 100
                result.energy = 100
                result.nowhp = result.hp
                result.save()
                er.save()
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            elif (int(er.nowhp) <= 0):
                gold, exp, sometext = db.winner(idp, location)
                text = str(call.message.text)
                text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
                result.battleStatus = 0
                er.battleStatus = 0
                er.nowhp = er.hp
                result.progStatus = 1
                result.save()
                er.save()
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif do == 'kazn':
        result = db.Users.get(user_id=call.from_user.id)
        idp = result
        location = result.location
        er = db.Monsters.get(id=result.battleWith)
        fullHpMob = int(er.hp)
        needHpToSkill = fullHpMob * 0.13
        if int(er.nowhp) <= needHpToSkill:
            pass
        else:
            bot.send_message(call.message.chat.id, "Недоступно. У моба hp больше необходимого.")
            return
        energy = result.energy
        if (int(energy) - 20) >= 0:
            result.energy = result.energy - 20
            result.save()
        else:
            result.energy = 0
            result.eat = result.eat - 8
            result.save()
        gold, exp, sometext = db.winner(idp, location)
        text = str(call.message.text)
        text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
        result.battleStatus = 0
        result.progStatus = 1
        er.battleStatus = 0
        er.nowhp = er.hp
        er.save()
        result.save()
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    elif do == 'shoot':
        result = db.Users.get(user_id=call.from_user.id)
        idp = result
        location = result.location
        shootAtk = int(result.atk * 1.5)
        er = db.Monsters.get(id=result.battleWith)
        er.nowhp = er.nowhp - shootAtk
        if (int(er.nowhp) <= 0):
            gold, exp, sometext = db.winner(idp, location)
            text = str(call.message.text)
            text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
            result.battleStatus = 0
            er.battleStatus = 0
            er.nowhp = er.hp
            result.progStatus = 1
            result.save()
            er.save()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            er.save()
            text = str(call.message.text)
            text += "\nВы нанесли {} урона выстрелом. У врага осталось {} hp. Битва продолжается".format(str(shootAtk), er.nowhp)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            pIdName = "Свиток телепортации"
            o = db.Inventory.get(active=1, name=pIdName, idplayer=result.id)
            if o:
                markup.add(InlineKeyboardButton('Телепортация в город', callback_data="battle_tp"))
            else:
                markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
    elif do == 'oneshot':
        result = db.Users.get(user_id=call.from_user.id)
        idp = result
        location = result.location
        er = db.Monsters.get(id=result.battleWith)
        kill = random.randint(0, 100)
        if kill <= 75:
            gold, exp, sometext = db.winner(idp, location)
            text = str(call.message.text)
            text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
            er.nowhp = er.hp
            result.battleStatus = 0
            er.battleStatus = 0
            result.progStatus = 1
            er.save()
            result.save()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            text = str(call.message.text)
            text += "\nВы промахнулись"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            pIdName = "Свиток телепортации"
            o = db.Inventory.get(active=1, name=pIdName, idplayer=result.id)
            if o:
                markup.add(InlineKeyboardButton('Телепортация в город', callback_data="battle_tp"))
            else:
                markup.add(InlineKeyboardButton('Телепортация(Недоступно)', callback_data="battle_tpOff"))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
    elif do == 'seriya':
        random1 = random.randint(0, 100)
        random2 = random.randint(0, 100)
        random3 = random.randint(0, 100)
        res = db.Users.get(user_id=call.from_user.id)
        er = db.Monsters.get(id=res.battleWith)
        idp = res
        atk = int(res.atk)
        location = res.location
        newAtk = int(atk * 2)
        oldAtk = int(atk * 0.3)
        text = str(call.message.text)
        if random1 >= 20:
            er.nowhp = er.nowhp - newAtk
            text += "\nПервый удар: {} урона".format(str(newAtk))
        else:
            er.nowhp = er.nowhp - oldAtk
            text += "\nПервый удар: {} урона".format(str(oldAtk))
        if random2 >= 20:
            er.nowhp = er.nowhp - newAtk
            text += "\nВторой удар: {} урона".format(str(newAtk))
        else:
            er.nowhp = er.nowhp - oldAtk
            text += "\nВторой удар: {} урона".format(str(oldAtk))
        if random3 >= 20:
            er.nowhp = er.nowhp - newAtk
            text += "\nТретий удар: {} урона".format(str(newAtk))
        else:
            er.nowhp = er.nowhp - oldAtk
            text += "\nТретий удар: {} урона".format(str(oldAtk))
        er.save()
        if int(er.nowhp) > 0:
            text += "\nУ противника осталось {} ед здоровья. Битва продолжается".format(str(er.nowhp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            markup.add(InlineKeyboardButton('Телепортация в город', callback_data="battle_tp"))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
        else:
            result.battleStatus = 0
            er.battleStatus = 0
            er.nowhp = er.hp
            result.progStatus = 1
            result.save()
            er.save()
            gold, exp, sometext = db.winner(idp, location)
            text = str(call.message.text)
            text += "\n\nМонстр повержен\n\n Получено: 💰{} золота и ✨{} опыта\n{}".format(str(gold), str(exp), str(sometext))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
