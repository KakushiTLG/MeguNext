import pymysql
@bot.message_handler(commands=['addmob'])
def addmob(m):
    if str(m.from_user.id) in owner:
        mob = m.text.replace('/addmob', '', 1).split(':')
        try: 
        	print(mob[5])
        except:
        	bot.reply_to(m, "/addmob имя:атака:хп:локация:макс опыт:макс голда")
        	return
        _ = pymysql.connect(host='localhost',
                         user='rabbit',
                         password='password',                             
                         db='megu',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
        with _.cursor() as cursor:
            sql = "SELECT pos FROM monsters WHERE location = %s ORDER BY pos DESC"
            cursor.execute(sql, (mob[3]))
            currentpos = cursor.fetchone()
            _.close()
        newpos = currentpos['pos'] + 1
        newmob = db.Monsters(name=mob[0], atk=mob[1], hp=mob[2], nowhp=mob[2], battleStatus=0, battleWith=0, location=mob[3], pos=newpos, maxexp=mob[4], maxgold=mob[5])
        newmob.save()
        if newmob:
            bot.reply_to(m, "Моб добавлен. \nИмя {}\natk {}\nhp {}\nlocation {}\n pos {}\n max exp {}\nmax gold {}".format(newmob.name, newmob.atk, newmob.hp, newmob.location, newmob.pos, newmob.maxexp, newmob.maxgold))

@bot.message_handler(commands=['adddonate'])
def adddonate(m):
    if str(m.from_user.id) in owner:
        text = m.text.replace("/adddonate ", "", 1).split(":")
        userId = text[0]
        plusPts = int(text[1])
        user = db.Users.get(user_id=userId)
        if user:
            pass
        else:
            user = db.Users.get(id=userId)
        user.almaz = user.almaz + plusPts
        user.donatesum = user.donatesum + plusPts
        if user.ref:
            toPay = int(plusPts * 0.1)
            ref = db.Users.get(user_id=user.ref)
            ref.almaz = ref.almaz + toPay
            if ref.partner == 1:
                user.donatesumPartn = user.donatesumPartn + plusPts
            ref.save()
        user.save()
        bot.send_message(m.chat.id, "Добавлен донат на {} от игрока {}".format(plusPts, user.username))


@bot.message_handler(commands=['ownpanel'])
def ownpanel(m):
    if str(m.from_user.id) in owner:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Статистика', callback_data="ownpanel_stats"))
        markup.add(InlineKeyboardButton('Качалка', callback_data="ownpanel_kach"))
        bot.send_message(m.chat.id, "Админ-панель", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('ownpanel_'))
def ownpanelcheck(call): 
    nav = call.data.split('_')
    q = nav[1]
    if q == 'stats':
        battless = db.Battle.select().order_by(db.Battle.id.desc()).limit(1)
        for battles in battless:
            battlesId = battles.id
        allusrs = db.Users.select()
        usersAll = 0
        usrA = 0
        for allusers in allusrs:
            usersAll += 1
            if allusers.location != 'Город' and allusers.location != 'Хэвенбург':
                usrA += 1
        activeusers = db.Users.select().where(db.Users.sleepPlayer>=time.time())
        countActive = 0
        for z in activeusers:
            countActive += 1
        trade = db.Trades.select().order_by(db.Trades.id.desc()).limit(1)
        for trades in trade:
            tradeId = trades.id
        invs = db.Inventory.select().order_by(db.Inventory.id.desc()).limit(1)
        for i in invs:
            iId = i.id
        text = "Статистика:\nСыграно битв: {}\nКоличество игроков: {}\nИгроков вне города: {}\nАктивных за последние сутки: {}\nВсего трейдов: {}\nВсего айтемов: {}".format(battlesId, usersAll, usrA, countActive, tradeId, iId)
        users = db.Users.select().order_by(db.Users.lvl.desc()).limit(5)
        text += "\n\nТоп игроков по уровню:\n"
        for z in users:
            text += "\n{} - {}lvl".format(z.username, z.lvl)
        users = db.Users.select().order_by(db.Users.money.desc()).limit(5)
        text += "\n\nТоп игроков по голде:\n"
        for z in users:
            text += "\n{} - {}💰".format(z.username, z.money)
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif q == 'kach':
        text = "Choose"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Обновить результаты', callback_data="admin_kach_refresh"))
        markup.add(InlineKeyboardButton('Сделать итоги конкурса', callback_data="admin_kach_result"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def ownpanelcheck(call): 
    nav = call.data.split('_')
    q = nav[1]
    if q == 'kach':
        q = nav[2]
        if q == 'refresh':
            conn = peewee.mysql.connect(host='localhost', user='rabbit', password='password', database='megu')
            conn.cursor().execute('TRUNCATE `temp`;')
            conn.close()
            users = {}
            f = open('1.txt', 'r').read()
            d = f.splitlines()
            for z in d:
                try:
                    users[z] += 1
                except:
                    users[z] = 1
            for z in users:
                check = db.Temp(user_id=z, count=users[z])
                check.save()
            usrs = db.Temp.select().order_by(db.Temp.count.desc()).limit(5)
            text = ""
            for z in usrs:
                user = db.Users.get(user_id=z.user_id)
                text += "\n{} - {}".format(user.username, z.count)
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        elif q == 'result':
            conn = peewee.mysql.connect(host='localhost', user='rabbit', password='password', database='megu')
            conn.cursor().execute('TRUNCATE `temp`;')
            conn.close()
            users = {}
            f = open('1.txt', 'r').read()
            d = f.splitlines()
            for z in d:
                try:
                    users[z] += 1
                except:
                    users[z] = 1
            for z in users:
                check = db.Temp(user_id=z, count=users[z])
                check.save()
            usrs = db.Temp.select().order_by(db.Temp.count.desc()).limit(3)
            count = 0
            text = "Неделя завершается, а вместе с ней и завершается конкурс #0 в качалке!\nПоказываем вам ТОП-3 игроков по активности в качалке!"
            for z in usrs:
                count += 1
                if count == 1: s = '🥇'
                elif count == 2: s = '🥈'
                elif count == 3: s = '🥉'
                user = db.Users.get(user_id=z.user_id)
                text += "\n{}{} - {}ед.{}".format(s, user.username, z.count, s)
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



@bot.message_handler(commands=['report'])
def report(m):
    user = db.Users.get(user_id=m.from_user.id)
    if user and user.ban == 1:
        profile(m)
        return
    if m.from_user.id == m.chat.id:
        gg = bot.send_message(m.chat.id, "Хорошо! Напишите, что хотите сообщить разработчику.")
        bot.register_next_step_handler(gg, report1)

def report1(m):
    user = db.Users.get(user_id=m.from_user.id)
    bot.send_message(devChat, "Репорт от {} , {}\n{}".format(m.from_user.id, user.username, m.text))
    bot.reply_to(m, "Сообщение отправлено. Спасибо!")

@bot.message_handler(commands=['answer'])
def answer(m):
    if str(m.from_user.id) in owner:
        text = m.text.replace("/answer ", "", 1)
        __user_id = m.reply_to_message.text.replace("Репорт от ", "", 1)
        _user_id = __user_id.split(" ")
        user_id = _user_id[0]
        bot.send_message(user_id, "⚠️На ваше сообщение пришёл ответ от разработчика!⚠️\n{}".format(text))
       	bot.reply_to(m, "Запрос закрыт")

@bot.message_handler(commands=["user"])
def user(m):
    if (m.from_user.id == kakushigoto):
        userid = int(m.text.split(maxsplit=1)[1])
        UsrInfo = bot.get_chat_member(userid, userid).user
        bot.send_message(kakushigoto, "Id: " + str(UsrInfo.id) + "\nFirst Name: " + str(UsrInfo.first_name) + "\nLast Name: " + str(UsrInfo.last_name) +
                            "\nUsername: @" + str(UsrInfo.username))

@bot.message_handler(commands=['ban'])
def ban(m):
    if str(m.from_user.id) in owner:
        text = m.text.replace("/ban ", "", 1)
        user = db.Users.get(user_id=int(text))
        if user:
            user.ban = 1
            user.save()
        else:
            user = db.Users(user_id=text, ban=1, username='bannedUser', item='БАНХАММЕР')
            user.save()
        bot.reply_to(m, "BANNED")

@bot.message_handler(commands=['getuser'])
def getuser(m):
    if str(m.from_user.id) in owner:
        user_id = m.text.replace("/getuser ", "", 1)
        user = db.Users.get(username=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
            if user:
                pass
            else:
                user = db.Users.get(user_id=user_id)
                if user:
                	pass
                else:
                	bot.reply_to(m, "Игрока не существует")
                	return
        _itemAtk = user.lvl / 100
        if user.item == "Пистолет с ножом":
            playerAtk = int(user.atk * 0.3)
        elif user.item == "Копьё":
            playerAtk = int(user.atk * 0.4)
        else:
            itemAtk = 1 + _itemAtk
            playerAtk = int(int(user.atk * itemAtk) - user.atk)
        needexp = user.lvl * 100
        text = "👤{}\n".format(user.username)
        if user.location == 'Город':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        else:
            text += "📡*{}*\n".format(user.location)
        text += "🔆{} (✨*{}/{}*)\n\n".format(user.lvl, user.exp, needexp)
        text += "❤️{}/{} 🛡{}\n".format(user.nowhp, user.hp, user.armor)
        text += "🔪{}(+{})\n".format(user.atk, int(playerAtk))
        text += "⚡️{}/100 🍗{}/100\n\n".format(user.energy, user.eat)
        text += "💰{} 💎{}\n".format(user.money, user.almaz)
        text += "🗡Экипировано: {}\n\n".format(user.item)
        text += "🤝{} ⭐️{}/5\n\n".format(user.tradecount, user.tradenum)
        text += "🆔 - {}".format(user.id)
        text += "🧩 - {}".format(user.frak)
        text += "\n\n\nbattleStatus {}\nprogLoc/status {}/{}".format(user.battleStatus, user.progLoc, user.progStatus)
        if user.ban != 0 and user.ban != 2:
            text += "\n⛔️Banned⛔️\n{}".format(user.banreason)
        gg = bot.get_chat_member(-1001345068459, user.user_id).status
        if gg == 'left':
            text += "\nГруппа ❌"
        else:
            text += "\nГруппа ✅"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Инвентарь игрока', callback_data="getuser_inventory_{}".format(user_id)))
        markup.add(InlineKeyboardButton('Дать 50 голды', callback_data="getuser_givegold_{}".format(user_id)))
        markup.add(InlineKeyboardButton('Выдать 1 кристалл', callback_data="getuser_givealmaz_{}".format(user_id)))
        markup.add(InlineKeyboardButton('SET battleStatus 0', callback_data="getuser_battlestatus_{}".format(user_id)))
        markup.add(InlineKeyboardButton('SET location Heavenburg', callback_data="getuser_gogorod_{}".format(user_id)))
        markup.add(InlineKeyboardButton('SET location start city', callback_data="getuser_gorod_{}".format(user_id)))
        if user.ban == 0 or user.ban == 2:
            markup.add(InlineKeyboardButton('Забанить игрока', callback_data="getuser_ban_{}".format(user_id)))
        else:
            markup.add(InlineKeyboardButton('Разбанить игрока', callback_data="getuser_ban_{}".format(user_id)))
        bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)
tempgg = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('getuser_'))
def getuser(call): 
    if str(call.from_user.id) in owner:
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    user_id = do[2]
    if use == 'inventory':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        inventory = db.Inventory.select().where(db.Inventory.idplayer == user.id, db.Inventory.active!= 0)
        inventorySize = db.getInventorySize(user)
        text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
        for item in inventory:
            text += "\n{} - active={}".format(item.name, item.active)
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'givegold':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        user.money += 50
        user.save()
        text = "Выдано 50 голды"
        try:
            bot.send_message(user.user_id, "Вам было зачислено 50💰")
        except:
            pass
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'battlestatus':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        user.battleStatus = 0
        user.save()
        text = "SET battleStatus = 0"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'gogorod':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        user.location = 'Хэвенбург'
        user.save()
        text = "SET location Heavenburg"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'gorod':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        user.location = 'Город'
        user.save()
        text = "SET location Город"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'givealmaz':
        user = db.Users.get(user_id=user_id)
        if user:
            pass
        else:
            user = db.Users.get(id=user_id)
        user.almaz += 1
        user.save()
        bot.send_message(kakushigoto, "{} зачислил 1 алмаз игроку {}".format(call.from_user.username, user.username))
        text = "Выдан кристалл"
        try:
            bot.send_message(user.user_id, "Вам был зачислен 1💎 за активность!")
        except:
            pass
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif use == 'ban':
        user = db.Users.get(user_id=user_id)
        if user.ban != 0 and user.ban != 2:
            user.ban = 2
            user.save()
            text = "Бан снят"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            gg = bot.send_message(call.message.chat.id, "Введите причину бана {}".format(user_id))
            global tempgg
            tempgg = gg
            bot.register_next_step_handler(gg, ban_reason)



def ban_reason(m):
    if str(m.from_user.id) in owner:
        global tempgg
        user_id = tempgg.text.replace("Введите причину бана ", "", 1)
        user = db.Users.get(user_id=user_id)
        user.banreason = m.text
        user.ban = 1
        user.save()
        bot.reply_to(m, "Игрок {} забанен с причиной:\n{}".format(user.username, m.text))
        try:
        	bot.send_message(user.user_id, "Поздравляем! Вы были забанены с причиной:\n{}".format(m.text))
        except:
        	pass

@bot.message_handler(commands=['notification'])
def ownnotification(m):
    if str(m.from_user.id) in owner:
        count = 0
        success = 0
        text = m.text.replace("/notification ", "", 1)
        users = db.Users.select()
        for z in users:
            try:
                bot.send_message(z.user_id, text)
                success += 1
            except:
                pass
            count += 1
        bot.reply_to(m, "Рассылка завершена. Письмо получили {}/{} игроков".format(success, count))


@bot.message_handler(commands=['owncheck'])
def owncheck(m):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checkingowner(m))

async def checkingowner(m):
    if str(m.from_user.id) in owner:
        count = 0
        success = 0
        users = db.Users.select()
        for z in users:
            try:
                bot.send_chat_action(z.user_id, 'typing')
                success += 1
            except:
                pass
            count += 1
        bot.send_message(devChat, "Статистика. Активно {}/{} игроков".format(success, count))

