def profile(m):
    user = db.Users.get(user_id=m.from_user.id)
    if user:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        item1 = types.KeyboardButton('Профиль')
        item2 = types.KeyboardButton('Инвентарь')
        item4 = types.KeyboardButton('Навигация')
        if user.frak:
            item5 = types.KeyboardButton('Группировка')
            markup.row(item1, item2)
            markup.row(item4, item5)
        else:
            markup.row(item1, item2)
            markup.row(item4)
        _itemAtk = user.lvl / 100
        if user.item == "Пистолет с ножом":
            playerAtk = int(user.atk * 0.3)
        elif user.item == "Копьё":
            playerAtk = int(user.atk * 0.4)
        else:
            itemAtk = 1 + _itemAtk
            playerAtk = int(int(user.atk * itemAtk) - user.atk)
        needexp = user.lvl * 100
        if user.frak == 'Грязное небо': text = "🌋[{}](tg://user?id={})\n".format(user.username, user.user_id)
        elif user.frak == 'Вавилон': text = "🗼[{}](tg://user?id={})\n".format(user.username, user.user_id)
        elif user.frak == 'Хранители': text = "💠[{}](tg://user?id={})\n".format(user.username, user.user_id)
        elif user.frak == 'Небесные рыцари': text = "⚔️[{}](tg://user?id={})\n".format(user.username, user.user_id)
        else: text = "👤[{}](tg://user?id={})\n".format(user.username, user.user_id)
        if user.location == 'Город':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        elif user.location == 'Хэвенбург':
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
        if user.ban != 0 and user.ban != 2:
            text += "\n⛔️*BANNED*⛔️"
        bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)

#################
#   INVENTORY   #
#################
pechene = ['Записка из печенья гласит: _Ваша улыбка обладает невероятной силой.\nОтпугивать окружающих._', 'Записка из печенья гласит: _Трижды хлопни, прошепчи "Натурал", потряси правой рукой, а теперь проверь свой инвентарь._', 'Записка из печенья гласит: _Сегодня вам может повезти. А может и не повезти_\n¯\_(ツ)_/¯',
    'Записка из печенья гласит: _ОНИ ДЕРЖАТ МЕНЯ В ЗАЛОЖНИКАХ И ЗАСТАВЛЯЮТ ПОСТОЯННО ПРИДУМЫВАТЬ ТЕКСТЫ ДЛЯ ЭТОГО ПЕЧЕНЬЯ, ПОМОГИТЕ!_', 'Записка из печенья гласит: _Не гневи разработчика, он может засунуть тебе хер огра в такие места, о которых ты и не догадывался._', 'Записка из печенья гласит: _На тебя сегодня упадёт пианино, будь осторожен._',
    'Записка из печенья гласит: _ЗДОХНЕШ!_', 'Записка из печенья гласит: _Звёзды говорят... Козерога в этом месяце ждёт успех и процветание._', 'Записка из печенья гласит: _Бип. Бросьте монетку, чтобы получить предсказание. Буп._', 'Записка из печенья гласит: _Герой, судьба твоя трудна. На твоём пути к счастью препятствия будут появляться одно за другим... Но, в конце концов, ты обретёшь то, чего всегда желал, герой._',
    'Записка из печенья гласит: _И всё поглотит пламя._', 'Записка из печенья гласит: _\nКартофель 1 кг \nМасло сливочное \nКетчуп \nМакароны \nЯйца_', 'Записка из печенья гласит: _Игры кончились, у тебя 24 часа чтобы погасить долг. У нас твои близкие и лучше тебе поторопиться, пока с ними не случилось чего-то._',
    'Записка из печенья гласит: _Проснитесь и пойте, проснитесь и пойте._', 'Записка из печенья гласит: _Отдай девчонку и долг будет прощен._', 'Записка из печенья гласит: _Свалка таит в себе куда более ценные скоровища, чем кажется на первый взгляд._',
    'Записка из печенья гласит: _В этом печенье был очень сильный яд, который через три дня заставит твои внутренности плавиться, кожу облазить, а кости ломаться под малейшей нагрузкой. Положи 900 золота возле камня слева от тебя и мы отдадим тебе антидот. Ты конечно можешь и не верить, но кто знает, чем все это обернётся._',
    'Записка из печенья гласит: _Порой нужно отдавать, не ожидая получить что-то взамен._', 
    'Записка из печенья гласит: _Если появится возможность - воспользуйся ею._', 'Записка из печенья гласит: _В любой непонятной ситуации закупайся свитками телепортации._', 'Записка из печенья гласит: _Мы узнали твоё настоящее имя! Тебе не уйти_']

def inventory(m):
    user = db.Users.get(user_id=m.from_user.id)
    inventory = db.Inventory.select().where(db.Inventory.idplayer == user.id, db.Inventory.active== 1)
    inventorySize = db.getInventorySize(user)
    count = {}
    size1 = {}
    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for item in inventory:
        if item.name in count:
            name, size, bonus = db.items(item.name, check=True)
            count[item.name] += 1
            size1[item.name] = size1[item.name] + int(size)
        else:
            name, size, bonus = db.items(item.name, check=True)
            count[item.name] = 1
            size1[item.name] = int(size)
            markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item.id))))
    for dict in count:
        name, size, bonus = db.items(dict, check=True)
        text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
    check_a = db.Inventory.get(active=2, idplayer=user.id)
    if check_a:
        markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
    bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('invUse_'))
def invUse(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    result = db.Inventory.get(id=use)
    if result.type == 'Еда':
        text = "{}\n+🦴{}сытости.\nИспользовать?".format(str(result.name), str(result.bonus))
        markup.add(InlineKeyboardButton('Съесть'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Хлам":
        text = "{}. \nСудя по всему, хлам.".format(str(result.name))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Зелье":
        text = "{}. Использовать?".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Сундук":
        text = "{}. Открыть?".format(result.name)
        markup.add(InlineKeyboardButton('Открыть'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Артефакт":
        if result.name == 'Амулет здоровья':
            text = "{}. Позволяет пассивно восстанавливать каждую минуту 5❤️ в обмен на 3⚡️. Необходимо надеть.".format(result.name)
        elif result.name == 'Осколок энергии':
            text = "{}. Позволяет пассивно восстанавливать каждую минуту 5⚡️, если энергия выше 5⚡️, но не выше 60⚡️".format(result.name)
        elif result.name == 'Кольцо живости':
            text = "{}. Благодаря специальной ауре увеличивает ❤️ на 15%.".format(result.name)
        else:
            text = "{}. Действие неизвестно".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Броня":
        name, size, bonus = db.items(result.name, check=True)
        text = "{}. +{}🛡 Использовать?".format(name, bonus)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    else:
        text = "{}. \nИспользовать?".format(str(result.name))
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('invDrop_'))
def invDrop(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    result = db.Inventory.get(id=use)
    result.active = 0
    result.save()
    text = "Вы выбросили {}".format(result.name)
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)





@bot.callback_query_handler(func=lambda call: call.data.startswith('invUsing_'))
def invUsing(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    result = db.Inventory.get(id=use)
    user = db.Users.get(id=result.idplayer)
    if result.active != 0:
        pass
    else:
        text = "Предмета не существует!"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    if result.type == 'Еда':
        result.active = 0
        user.eat = user.eat + result.bonus
        if int(user.eat) > 100:
            user.eat = 100
        if result.name == 'Печенье с предсказанием':
            text = "Приятного аппетита!\n{}".format(random.choice(pechene))
        else:
            text = "Приятного аппетита!\n"
        if result.name == "🥠 Печенье с предсказанием":
            name = user.username
            username = call.from_user.first_name
            pr = db.predskaz(name, username)
            text += str(pr)
    elif result.name == 'Свиток телепортации':
        if user.location == 'Первый этаж башни' or user.location == 'Второй этаж башни' or user.location == 'Третий этаж башни' or user.location == 'Четвёртный этаж башни':
            text = "Вы попытались сбежать от гнева монстров башни, однако произнесённое заклинание не помогло - вы остались внутри башни."
            return text
        if user.battleStatus == 1:
            mob = db.Monsters.get(id=user.battleWith)
            if mob:
                mob.battleStatus = 0
                mob.nowhp = mob.hp
                mob.save()
                user.battleStatus = 0
        result.active = 0
        checkgorod = db.Inventory.get(idplayer=user.id, name='Большой город')
        if checkgorod:
            user.location = 'Хэвенбург'
        else:
            user.location = 'Город'
        user.position = 'Площадь'
        user.battleStatus = 0
        text = "Вы использовали 📜Свиток телепортации"
    elif result.name == 'Кофе':
        result.active = 0
        user.energy = user.energy + 70
        if user.energy > 100:
            user.energy = 100
        text = "Вы использовали ☕️Кофе"
    elif result.name == 'Зелье восстановления':
        result.active = 0
        user.nowhp = user.hp
        text = "Вы использовали 🧪Зелье восстановления"
    elif result.type == 'Зелье':
        result.active = 0
        user.nowhp = user.nowhp + result.bonus
        if user.nowhp > user.hp:
            user.nowhp = user.hp
        text = "Вы успешно использовали {}".format(str(result.name)) 
    elif result.type == 'Сундук':
        text = case(result)
    elif result.type == 'Броня':
        user = db.Users.get(user_id=call.from_user.id)
        text = armoruse(call, use, result, user)
    elif result.type == 'Артефакт':
        user = db.Users.get(user_id=call.from_user.id)
        text = userart(call, use, result, user)
        user = db.Users.get(user_id=call.from_user.id)
    else:
        text = "В разработке"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Инвентарь', callback_data="inv"))
    result.save()
    user.save()
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('inv'))
def inv(call):
    user = db.Users.get(user_id=call.from_user.id)
    inventory = db.Inventory.select().where(db.Inventory.idplayer == user.id, db.Inventory.active == 1)
    inventorySize = db.getInventorySize(user)
    count = {}
    size1 = {}
    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for item in inventory:
        if item.name in count:
            name, size, bonus = db.items(item.name, check=True)
            count[item.name] += 1
            size1[item.name] = size1[item.name] + int(size)
        else:
            name, size, bonus = db.items(item.name, check=True)
            count[item.name] = 1
            size1[item.name] = int(size)
            markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item.id))))
    for dict in count:
        name, size, bonus = db.items(dict, check=True)
        text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
    check_a = db.Inventory.get(active=2, idplayer=user.id)
    if check_a:
        markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)




@bot.callback_query_handler(func=lambda call: call.data.startswith('inveClose'))
def invClose(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    text = "Вы закрыли инвентарь"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


#################
# ARMOR & ARTS  #
#################
def userart(call, use, result, user):
    if result.name == 'Кусок паззла':
        result.active = 0
        user.atk += 10
        user.save()
        result.save()
        text = "Не зная что делать с этим кусочком паззла, вы случайно сломали его. Внезапно, вы почувствовали лёгкость и головокружение, а вокруг паззла появилось странное свечение, которое разгоралось всё ярче и ярче. Когда свет пропал, паззла вы не обнаружили.\n+10🔪"
    elif result.name == 'Волшебные кости':
        text = "Вы просто... Бросили кости на пол, глядя на комбинацию. Но ничего не случилось. Пришлось их подобрать... Наверное, нужно их оставить до лучшего момента."
    elif result.name == 'Амулет здоровья':
        checkother = db.Inventory.get(idplayer=user.id, name='Амулет здоровья', active=2)
        checkother2 = db.Inventory.get(idplayer=user.id, name='Осколок энергии', active=2)
        if result.active == 2:
            result.active = 1
            result.save()
            text = "Вы успешно сняли {}".format(result.name)
            return text
        if checkother or checkother2:
            text = "У вас уже есть амулет, который используется"
        else:
            text = "Вы надели 🧿Амулет здоровья"
            result.active = 2
            result.save()
    elif result.name == 'Осколок энергии':
        checkother = db.Inventory.get(idplayer=user.id, name='Осколок энергии', active=2)
        checkother2 = db.Inventory.get(idplayer=user.id, name='Амулет здоровья', active=2)
        if result.active == 2:
            result.active = 1
            result.save()
            text = "Вы успешно сняли {}".format(result.name)
            return text
        if checkother or checkother2:
            text = "У вас уже есть амулет, который используется"
        else:
            text = "Вы надели 🔷Осколок энергии"
            result.active = 2
            result.save()
    elif result.name == 'Кольцо живости':
        if result.active == 1:
            result.active = 2
            userBonusHp = user.hp * 0.15
            user.hp += int(userBonusHp)
            user.save()
            result.save()
            text = "Вы надели 💍Кольцо живости"
        else:
            result.active = 1
            userBonusHp = user.hp / 1.15
            user.hp = int(userBonusHp)
            user.save()
            result.save()
            text = "Вы сняли 💍Кольцо живости"
    return text


@bot.callback_query_handler(func=lambda call: call.data.startswith('armorpers'))
def armorpers(call):
    user = db.Users.get(user_id=call.from_user.id)
    re = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.active==2)
    text = 'Снаряжение, что вы носите:'
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for z in re:
        if z.type == 'Броня':
            name, bonus, size = db.items(z.name, check=True)
            text += "\n{} | +{}🛡".format(name, z.bonus)
        elif z.type == 'Артефакт':
            name, bonus, size = db.items(z.name, check=True)
            text += "\n{}".format(name)
        markup.add(InlineKeyboardButton('Снять {}'.format(name), callback_data="invUsing_{}".format(z.id)))
    markup.add(InlineKeyboardButton('В инвентарь', callback_data="invClose"))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)



def armoruse(call, use, result, user):
    head = ['Хоккейная маска', 'Кожаный шлем', 'Шляпа фокусника', 'Кепка адидас', 'Шлем из фольги', 'Колпак главврача']
    body = ['Кожаный нагрудник', 'Бронежилет', 'Комбинезон сталкера', 'Ночнушка Раскуловой', 'Майка из пакета', 'Халат главрача']
    foot = ['Кожаные штаны', 'Спортивки адидас', 'Нижнее бельё Раскуловой', 'Штаны Ашодас', 'Модные штаны', 'Штаны главврача']
    shoes = ['Берцы', 'Кожаные ботинки', 'Кросы адидас', 'Туфельки Раскуловой', 'НЕкроссовки', 'Тапочки главврача']
    nowhead = 1 if result.name in head else 0
    nowbody = 1 if result.name in body else 0
    nowfoot = 1 if result.name in foot else 0
    nowshoes = 1 if result.name in shoes else 0
    if result.active == 1:
        re = db.Inventory.select().where(db.Inventory.idplayer==result.idplayer, db.Inventory.active==2, db.Inventory.id!=result.id)
        for z in re:
            if z.name in head and nowhead == 1 or z.name in body and nowbody == 1 or z.name in foot and nowfoot == 1 or z.name in shoes and nowshoes == 1:
                text = "У вас уже одета другая броня подобного типа"
                return text
        result.active = 2
        user.armor = user.armor + result.bonus
        user.save()
        result.save()
        text = "Вы успешно надели броню."
    else:
        inventorySize = db.getInventorySize(user)
        if result.size + inventorySize > user.inventorySizeMax:
            text = "Единственное куда Вы можете деть снаряжение - в зубы, но оно достаточно большое для этого"
        else:
            result.active = 1
            user.armor = user.armor - result.bonus
            result.save()
            user.save()
            text = "Вы успешно сняли броню."
    return text


################################
#    REFERAL O4KA I DONATE     #
################################
@bot.message_handler(commands=['myrefs'])
def refs(m):
    result = db.Users.select().where(db.Users.ref==m.from_user.id)
    count = 0
    textc = ""
    for dict in result:
        count += 1
        donatesum = int(dict.donatesum * 0.1)
        textc += "{} - {}lvl. Доход: {}💎\n".format(dict.username, dict.lvl, donatesum)
    if count != 0:
        text = "Реферальная система:\nПри приглашении пользователя по специальной ссылке вы получите 150💰 при достижении им 5 уровня.\nПри донате приглашенного вами пользователя вы получаете 10%💎 от суммы доната.\nВаша специальная ссылка для приглашения:\n`https://t.me/TowerOfHeaven_bot?start={}`\nСписок ваших рефералов и дохода с них:\n{}".format(str(m.from_user.id), textc)
    else:
        text = "Реферальная система:\nПри приглашении пользователя по специальной ссылке вы получите 150💰 при достижении им 5 уровня.\nПри донате приглашенного вами пользователя вы получаете 10%💎 от суммы доната.\nВаша специальная ссылка для приглашения:\n`https://t.me/TowerOfHeaven_bot?start={}`\nУ вас нет рефералов в данный момент.".format(str(m.from_user.id))
    bot.reply_to(m, text, parse_mode='markdown')
import requests
mylogin = '380662357576'
api_access_token = 'f3e92f90802cacea83fd8183641edac9'

@bot.message_handler(commands=['donate'])
def donatestar(m):
    result = db.Users.get(user_id=m.from_user.id)
    res = db.Donate.get(user=m.from_user.id, status=0)
    if res:
        text = res.comment
    else:
        symbol = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        text = ''
        for i in range(20):
            text += random.choice(symbol)
        newdonate = db.Donate(user=m.from_user.id, summ=0, status=0, comment=text)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Проверить платёж', callback_data="checkdonate_{}_{}".format(result.id, text)))
    donateText = "Покупка 💎 совершается по курсу - 1 рубль = 1💎."
    donateText += "\nНа данный момент поддержка и покупка 💎 доступна только в ручном режиме ( https://yasobe.ru/na/TowerOfHeaven )\nВ комментарии платежа укажите Ваш внутриигровой ID - {} для зачисления на Ваш баланс 💎\nЗачисление 💎 произойдёт в течении суток (можете воспользоваться /report для ускорения процесса"
#    donateText += "\n⚠️ВНИМАТЕЛЬНО скопируйте код. В случае ошибки, автоматическое зачисление не пройдёт.⚠️"
#    donateText += "\nКод - `{}`".format(text)
    bot.send_message(m.chat.id, donateText, parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('donate_start'))
def donatestart(call):
    result = db.Users.get(user_id=call.from_user.id)
    res = db.Donate.get(user=call.from_user.id, status=0)
    if res:
        text = res.comment
    else:
        symbol = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        text = ''
        for i in range(20):
            text += random.choice(symbol)
        newdonate = db.Donate(user=call.from_user.id, summ=0, status=0, comment=text)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Проверить платёж', callback_data="checkdonate_{}_{}".format(result.id, text)))
    donateText = "Покупка 💎 совершается по курсу - 1 рубль = 1💎."
    donateText += "\nНа данный момент поддержка и покупка 💎 доступна только в ручном режиме ( https://yasobe.ru/na/TowerOfHeaven )\nВ комментарии платежа укажите Ваш внутриигровой ID - {} для зачисления на Ваш баланс 💎\nЗачисление 💎 произойдёт в течении суток (можете воспользоваться /report для ускорения процесса"
#    donateText += "\n⚠️ВНИМАТЕЛЬНО скопируйте код. В случае ошибки, автоматическое зачисление не пройдёт.⚠️"
#    donateText += "\nКод - `{}`".format(text)
    gg = bot.edit_message_text(donateText, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')




# История платежей - последние и следующие n платежей
def payment_history_last(my_login, api_access_token, rows_num, next_TxnId, next_TxnDate):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token  
    parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params = parameters)
    return h.json()


@bot.callback_query_handler(func=lambda call: call.data.startswith('checkdonate_'))
def checkdonate(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    id = do[1]
    key = do[2]
    lastPayments = payment_history_last(mylogin, api_access_token, '5','','')
    strat = False
    for dict in lastPayments:
        data = lastPayments['data']
        for list in data:
            summ = list['sum']
            amount = summ['amount']
            comment = list['comment']
            status = list['status']
            if status == "SUCCESS":
                if str(comment) == str(key):
                    strat = True
                    plusPts = int(amount)
                    bot.send_message(kakushigoto, "Успешный платёж\n{}/{} на {} руб".format(call.from_user.id, call.from_user.username, str(amount)))
                    try:
                        text = "Спасибо, платёж прошёл. Вам зачислено {} 💎".format(str(plusPts))
                        re = db.Donate.get(comment=key)
                        if re.status == 1:
                            text = "Ошибка. Обратитесь в /report"
                            return
                        else:
                            pass
                        user = db.Users.get(user_id=re.user)
                        user.almaz = user.almaz + plusPts
                        user.donatesum = user.donatesum + plusPts
                        re.status = 1
                        re.summ = plusPts
                        if user.ref:
                            toPay = int(plusPts * 0.1)
                            ref = db.Users.get(user_id=user.ref)
                            ref.almaz = ref.almaz + toPay
                            if ref.partner == 1:
                                user.donatesumPartn = user.donatesumPartn + plusPts
                        user.save()
                        re.save()
                        ref.save()
                        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)    
                        return
                    except:
                        text = "Не удалось зачислить 💎 на счёт. Обратитесь в /report с указанием комментария платежа\n{}".format(key)
                        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)    
                        return
    if strat == False:
        text = "Платёж не прошёл. Возможно, стоит немного подождать и попробовать снова нажать кнопку проверки платежа. Если же не помогает в течении долгого времени, обратитесь в /report для связи с разработчиком и ручным зачислением платежа с указанием кода оплаты..\nКлюч к комментарию платежа:\n"
        text += "`{}`\nQIWI-кошелёк: +380662357576".format(str(key))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Повторно проверить платёж.', callback_data="checkdonate_{}_{}".format(str(id), key)))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')
    





@bot.message_handler(commands=['mypartn'])
def mypartn(m):
    re = db.Users.get(user_id=m.from_user.id)
    if re.partner == 1:
        pass
    else:
        bot.reply_to(m, "Вы можете зарабатывать 30% от доната ваших рефералов. Для открытия функции обратитесь к разработчику - @kakushigoto")
        return
    result = db.Users.select().where(db.Users.ref == m.from_user.id)
    count = 0
    zarabotok = 0
    textc = ""
    for dict in result:
        count += 1
        zarabotok += int(dict.donatesumPartn * 0.3)
    text = "Ваша специальная ссылка для приглашения:\n`https://t.me/TowerOfHeaven_bot?start={}`\nПриглашено - {} чел.\nВсего заработано: {}руб.".format(str(m.from_user.id), count, zarabotok)
    bot.reply_to(m, text, parse_mode='markdown')

