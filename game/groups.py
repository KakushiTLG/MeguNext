def grouppanel(m):
    user = db.Users.get(user_id=m.from_user.id)
    if user.frak == 'Грязное небо': frakname = '🌋Грязное небо'
    elif user.frak == 'Вавилон': frakname = '🗼Вавилон'
    elif user.frak == 'Хранители': frakname = '💠Хранители'
    elif user.frak == 'Небесные рыцари': frakname = '⚔️Небесные рыцари'
    else: return
    fraka = str(user.frak)
    frak = db.Fraks.get(name=fraka)
    needExp = frak.lvl * 1000
    leader = db.Users.get(id=frak.leader)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = "{}\n🏆{}🏆\n\n✳️Уровень: {}\n❇️Опыт: {}/{}\n💰Фонд: {}\n👥Участников: {}\n\n\n🟣{}\n🔴{}\n🟢{}\n🔵{}".format(frakname, leader.username, frak.lvl, frak.exp, needExp, frak.fond, frak.players, frak.ametist, frak.rubin, frak.izumrud, frak.sapphire)
#    if leader.id == user.id:
#        markup.add(InlineKeyboardButton('Панель основателя', callback_data="fraka_panel"))
    markup.add(InlineKeyboardButton('Взнос в фонд', callback_data="fraka_pay"))
    checkNav = db.System.get(name='nav_fraka')
    if checkNav.value == 1:
        markup.add(InlineKeyboardButton('Поход к башне', callback_data="fraka_nav"))
    bot.reply_to(m, text, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('fraka_'))
def fraka(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    user = db.Users.get(user_id=call.from_user.id)
    fraka = db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if navWhere == "pay":
        try:
            summPay = nav[2]
            if user.money >= int(summPay):
                user.money -= int(summPay)
                fraka.fond += int(summPay)
                user.save()
                fraka.save()
                text = "Вы успешно внесли {}💰 в фонд".format(summPay)
            else:
                text = "У вас не хватает денег для взноса"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('100💰', callback_data="fraka_pay_100"))
            markup.add(InlineKeyboardButton('200💰', callback_data="fraka_pay_200"))
            markup.add(InlineKeyboardButton('500💰', callback_data="fraka_pay_500"))
            markup.add(InlineKeyboardButton('1000💰', callback_data="fraka_pay_1000"))
            gg = bot.edit_message_text("Выберите сумму для вклада в фонд группировки", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "nav":
        if user.location not in ['Тропа к башне', 'Башня', 'Первый этаж башни', 'Второй этаж башни', 'Третий этаж башни', 'Четвёртый этаж башни', 'Пятый этаж башни']:
            pass
        else:
            gg = bot.edit_message_text("Вы не можете отправиться туда повторно.", call.message.chat.id, call.message.message_id)
            return
        checkNav = db.System.get(name='nav_fraka')
        if checkNav.value == 1:
            user.location = "Тропа к башне"
            user.progLoc = "Тропа к башне|0"
            user.progStatus = 1
            user.save()
            gg = bot.edit_message_text("Вы отправились к башне", call.message.chat.id, call.message.message_id)
        else:
            gg = bot.edit_message_text("Сейчас там делать нечего", call.message.chat.id, call.message.message_id)





@bot.callback_query_handler(func=lambda call: call.data.startswith('tower_'))
def tower_(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    print(call.data)
    user = db.Users.get(user_id=call.from_user.id)
    nav = call.data.split('_')
    navWhere = nav[1]
    if navWhere == "2":
        if user.location == 'Первый этаж башни' and user.progLoc == 'Первый этаж башни|5' and user.nowhp > 0:
            user.location = 'Второй этаж башни'
            user.progLoc = 'Второй этаж башни|0'
            user.progStatus = 1
            text = "Вы перешли на второй этаж башни"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "3":
        if user.location == 'Второй этаж башни' and user.progLoc == 'Второй этаж башни|7' and user.nowhp > 0:
            user.location = 'Третий этаж башни'
            user.progLoc = 'Третий этаж башни|0'
            user.progStatus = 1
            text = "Вы перешли на третий этаж башни"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "4":
        if user.location == 'Третий этаж башни' and user.progLoc == 'Третий этаж башни|9' and user.nowhp > 0:
            user.location = 'Четвёртый этаж башни'
            user.progLoc = 'Четвёртый этаж башни|0'
            user.progStatus = 1
            text = "Вы перешли на четвёртый этаж башни"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "5":
        if user.location == 'Четвёртый этаж башни' and user.progLoc == 'Четвёртый этаж башни|11' and user.nowhp > 0:
            user.location = 'Пятый этаж башни'
            user.progLoc = 'Пятый этаж башни|0'
            user.progStatus = 1
            text = "Вы перешли на пятый этаж башни"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "6":
        if user.location == 'Пятый этаж башни' and user.progLoc == 'Пятый этаж башни|13' and user.nowhp > 0:
            user.location = 'Шестой этаж башни'
            user.progLoc = 'Шестой этаж башни|0'
            user.progStatus = 1
            text = "Вы перешли на шестой этаж башни"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    else:
        text = "Недоступно. Обратитесь в /report"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    user.save()
