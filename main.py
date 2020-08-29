gameActive = 1
def checker(m):
    user = db.Users.get(user_id=m.from_user.id)
    if user:
        user.sleepPlayer = int(time.time() + 86400)
        user.save()
        success = True
    else:
        start(m)
        success = False
    return success
antiflood = {}
activity = {}
@bot.message_handler(content_types=["text"])
def texthand(m):
    global antiflood
    global activity
    if gameActive == 0 and str(m.from_user.id) not in owner and m.chat.id == m.from_user.id:
        bot.reply_to(m, "Технические работы. Скоро всё заработает")
        return
    try:
        if antiflood[m.chat.id]:
            if antiflood[m.chat.id] > time.time():
                return
            else:
                antiflood[m.chat.id] = int(time.time()) + 2
    except:
        antiflood[m.chat.id] = int(time.time()) + 2
    if m.chat.id == m.from_user.id:
        success = checker(m)
        if success == True:
            user = db.Users.get(user_id=m.from_user.id)
            try:
                activity[m.from_user.id] += 1
                if activity[m.from_user.id] / 500 == activity[m.from_user.id] // 500:
                    bot.send_message(kakushigoto, "Игрок {} набрал 500 очков".format(user.id))
            except:
                activity[m.from_user.id] = 1
            if user.ban == 0:
                pass
            elif user.ban == 2:
                pass
            else:
                profile(m)
                return
            if m.text.lower() in ['профиль']:
                profile(m)
            elif m.text.lower() in ['инвентарь']:
                inventory(m)
            elif m.text.lower() in ['навигация']:
                navigation(m)
            elif m.text.lower() in ['рефералы']:
                refs(m)
            elif m.text.lower() in ['снаряжение']:
                inventory(m)
            elif m.text.lower() in ['группировка']:
                grouppanel(m)
        else:
            return

@bot.message_handler(content_types=['new_chat_members'])
def checkfrak(m):
    user = db.Users.get(user_id=m.from_user.id)
    if m.chat.id == -1001320424099: # Хранители
        if user and user.frak == 'Хранители':
            pass
        else:
            bot.kick_chat_member(m.chat.id, m.from_user.id)
    elif m.chat.id == -1001467052649: # Рыцари
        if user and user.frak == 'Небесные рыцари':
            pass
        else:
            bot.kick_chat_member(m.chat.id, m.from_user.id)
    elif m.chat.id == -1001121150202: # Грязное небо
        if user and user.frak == 'Грязное небо':
            pass
        else:
            bot.kick_chat_member(m.chat.id, m.from_user.id)
    elif m.chat.id == -1001336335908: # Вавилон
        if user and user.frak == 'Вавилон':
            pass
        else:
            bot.kick_chat_member(m.chat.id, m.from_user.id)
    elif m.chat.id == -1001345068459:
        user = db.Users.get(user_id=m.from_user.id)
        if user.ban != 2:
            user.money += 50
            user.ban = 2
            user.save()
            bot.send_message(user.user_id, "Вам было зачислено 50💰 за вступление в группу!")