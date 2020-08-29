def nick_parser(text, reg=True):
    count = 0
    txt = text
    symbols = 'qwertyuiopasdfghjklzxcvbnm'
    if reg:
        symbols += 'йёцукенгшщзхъфывапролджэячсмитьбю'
        symbols += '1234567890'
    try:
        _space = False
        for symbol in txt:
            if count >= 15:
                return txt
            count += 1
            if symbol in ' ' and not _space and reg:
                _space = True
            elif symbol.lower() not in symbols:
                txt = txt.replace(symbol, "")
            else:
                _space = False
    except:
        pass
    return txt

def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None
refcodes = {}
@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == m.chat.id:
        pass
    else:
        return
    checkplayer = db.Users.get(user_id=m.from_user.id)
    if checkplayer:
        profile(m)
        return
    else:
        unique_code = extract_unique_code(m.text)
        if not unique_code:
            unique_code = 702528084
        global refcodes
        refcodes[m.from_user.id] = unique_code
        bot.send_message(kakushigoto, "New user: @{} \n{}\nRef {}".format(m.from_user.username, m.from_user.id, refcodes[m.from_user.id]))
        text = "Здравствуй, одинокий странник, забредший в наши безлюдные пустоши. Eсли желаешь узнать побольше о здешних краях, дабы не плутать здесь как дурак, то прочитай этот древнейший документ одного из величайших старцев наших земель [ https://telegra.ph/Tower-of-Heaven-07-14-2 ] . Удачи тебе, не заблудись на первом же переулке."
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Катана', callback_data="registration_select_katana"))
        markup.add(InlineKeyboardButton('Меч', callback_data="registration_select_mech"))
        markup.add(InlineKeyboardButton('Пистолет с ножом', callback_data="registration_select_pistol"))
        markup.add(InlineKeyboardButton('Копьё', callback_data="registration_select_kopie"))
        bot.send_message(m.chat.id, text, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('registration_select_'))
def reg(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    item = do[2]
    global refcodes
    checkref = db.Users.get(user_id=refcodes[call.from_user.id])
    if checkref:
        pass
    else:
        refcodes[call.from_user.id] = 702528084
    if item == 'katana':
        user = db.Users(username=call.from_user.first_name, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0)
        if user:
            user.item = 'Катана'
            user.save()
            text = "Поздравляем с успешной регистрацией! В описании бота Вы можете найти ссылку на группу обсуждения игры (там Вы можете получить ответы на интересующие Вас вопросы по игре), а так же - новостной канал, чтобы быть в курсе всех обновлений.\nНапоминаем ссылку на гайд - https://telegra.ph/Tower-of-Heaven-07-14-2\nЕсли вдруг потеряете, воспользуйтесь командой /help\nПриятной игры."
            bot.send_message(call.message.chat.id, text)
            gg = bot.edit_message_text('Готово!', call.message.chat.id, call.message.message_id)
            gg = bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            bot.register_next_step_handler(gg, reg_nick)
    elif item == 'mech':
        user = db.Users(username=call.from_user.first_name, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0)
        if user:
            user.item = 'Меч'
            user.save()
            text = "Поздравляем с успешной регистрацией! В описании бота Вы можете найти ссылку на группу обсуждения игры (там Вы можете получить ответы на интересующие Вас вопросы по игре), а так же - новостной канал, чтобы быть в курсе всех обновлений.\nНапоминаем ссылку на гайд - https://telegra.ph/Tower-of-Heaven-07-14-2\nЕсли вдруг потеряете, воспользуйтесь командой /help\nПриятной игры."
            bot.send_message(call.message.chat.id, text)
            gg = bot.edit_message_text('Готово!', call.message.chat.id, call.message.message_id)
            gg = bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            bot.register_next_step_handler(gg, reg_nick)
    elif item == 'pistol':
        user = db.Users(username=call.from_user.first_name, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0)
        if user:
            user.item = 'Пистолет с ножом'
            user.save()
            text = "Поздравляем с успешной регистрацией! В описании бота Вы можете найти ссылку на группу обсуждения игры (там Вы можете получить ответы на интересующие Вас вопросы по игре), а так же - новостной канал, чтобы быть в курсе всех обновлений.\nНапоминаем ссылку на гайд - https://telegra.ph/Tower-of-Heaven-07-14-2\nЕсли вдруг потеряете, воспользуйтесь командой /help\nПриятной игры."
            bot.send_message(call.message.chat.id, text)
            gg = bot.edit_message_text('Готово!', call.message.chat.id, call.message.message_id)
            gg = bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            bot.register_next_step_handler(gg, reg_nick)
    elif item == 'kopie':
        user = db.Users(username=call.from_user.first_name, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0)
        if user:
            user.item = 'Копьё'
            user.save()
            text = "Поздравляем с успешной регистрацией! В описании бота Вы можете найти ссылку на группу обсуждения игры (там Вы можете получить ответы на интересующие Вас вопросы по игре), а так же - новостной канал, чтобы быть в курсе всех обновлений.\nНапоминаем ссылку на гайд - https://telegra.ph/Tower-of-Heaven-07-14-2\nЕсли вдруг потеряете, воспользуйтесь командой /help\nПриятной игры."
            bot.send_message(call.message.chat.id, text)
            gg = bot.edit_message_text('Готово!', call.message.chat.id, call.message.message_id)
            gg = bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            bot.register_next_step_handler(gg, reg_nick)
nicks = {}
def reg_nick(m):
    global nicks
    txt = nick_parser(m.text, reg=True)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.row(item1, item2)
    gg = bot.send_message(m.chat.id, 'Твоё имя - {}?'.format(txt), reply_markup=markup)
    nicks[m.from_user.id] = txt
    bot.register_next_step_handler(gg, reg_nick_1)

def reg_nick_1(m):
    global nicks
    if m.text == "Да":
        checknick = db.Users.get(username=nicks[m.from_user.id])
        if checknick and checknick.username == nicks[m.from_user.id]:
            gg = bot.send_message(m.chat.id, "К сожалению, такого героя мы уже знаем. Может, тебя зовут как-нибудь еще?\nЕсли это сообщение вылазит слишком часто, обратитесь в /report")
            bot.register_next_step_handler(gg, reg_nick)
            return
        user = db.Users.get(user_id=m.from_user.id)
        user.username = nicks[m.from_user.id]
        user.save()
        success = db.addItem('Сун-дук', user)
        bot.send_message(m.chat.id, '🏆 Получено достижение "Новичок"\nПолучен: 🧳Сун-дук')
        profile(m)
        bot.send_message(m.chat.id, "Вы можете получить еще один бонус! \nВступите в группу обсуждения игры ( @TowerOfHeaven_chat ) и получите бонус!")
    elif m.text == "Нет":
        gg = bot.send_message(m.chat.id, "Тогда назови своё настоящее имя!")
        bot.register_next_step_handler(gg, reg_nick)

@bot.callback_query_handler(func=lambda call: call.data.startswith('regcheckgroup'))
def regcheckgroup(call): 
    gg = bot.get_chat_member(-1001345068459, call.from_user.id).status
    if gg != 'left':
        user = db.Users.get(user_id=call.from_user.id)
        user.money += 50
        user.ban = 2
        user.save()
        text = "Получено: 50💰"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Проверить еще раз', callback_data="regcheckgroup"))
        text = "Вы не состоите в группе. Чтобы получить вознаграждение, Вам необходимо состоять в игровом чате @TowerOfHeaven_chat"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(m):
    bot.reply_to(m, "Tower of Heaven\nГайд от игрока - https://telegra.ph/Tower-of-Heaven-07-14-2 \nКанал игры (новости) - @TowerOfHeaven\nГруппа обсуждения игры - @TowerOfHeaven_chat\nКанал логирования действий в игре - @TowerOfHeaven_trades\nПомощь - /report")

"""
def restoring_reg(m):
    if m.forward_from:
        if m.forward_from.username == 'MeguNext_bot':
            pattern = r'👤(.+)\n.+\n🔆(\d+) \(✨(\d+)/\d+\)\n\n❤️(\d+/\d+).+\n🔪(\d+(\(\+\d+\))?)\n.+\n\n💰(\d+) 💎(\d+)\n🗡Экипировано: (([а-яА-я]+\s+)+)\n🆔 - \d+'
            result = re.match(pattern, m.text)
            print(result)
            if result:
                username = result[1]
                lvl = result[2]
                exp = result[3]
                _hp = result[4]
                __hp = _hp.split('/')
                hp = __hp[1]
                _atk = result[5].split('(')
                atk = _atk[0]
                money = result[7]
                almaz = result[8]
                item = result[9].replace('\n', '', 1)
                checkingplayer = db.Users.get(username=username)
                if checkingplayer:
                    bot.send_message(m.chat.id, 'Данный аккаунт уже был активирован. Повторная активация невозможна.')
                    start(m)
                    return
                user = db.Users(user_id=m.from_user.id, username=username, lvl=lvl, exp=exp, hp=hp, nowhp=hp, atk=atk, almaz=almaz, money=money, item=item, ban=0)
                user.save()
                bot.send_message(m.chat.id, 'Ваш профиль успешно восстановлен. Приятной игры!')
                profile(m)
            else:
                gg = bot.send_message(m.chat.id, 'Пожалуйста, перешлите сообщение с профилем из @MeguNext_bot для восстановления игрового персонажа.')
                bot.register_next_step_handler(gg, restoring_reg)
        else:
            gg = bot.send_message(m.chat.id, 'Пожалуйста, перешлите сообщение с профилем из @MeguNext_bot для восстановления игрового персонажа.')
            bot.register_next_step_handler(gg, restoring_reg)
    else:
        gg = bot.send_message(m.chat.id, 'Пожалуйста, перешлите сообщение с профилем из @MeguNext_bot для восстановления игрового персонажа.')
        bot.register_next_step_handler(gg, restoring_reg)
"""