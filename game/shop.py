def shop(m1, m2, m3):
    if db.System.get(name='shop_work').value == 0:
        gg = bot.edit_message_text('Вы подошли к магазину где стоял одинокий Ашот. \n_-Эй, Ашотик, брат, продай мне чё-нибудь\n-Пашёль нахуй_', m1, m3, parse_mode = 'markdown')
        return
    else:
        pass
    text = '_Ты подходишь к невзрачному стеллажу с выцвевшим навесом. Ощущение, словно владелец бросает в ящики для продуктов все, что находит по пути сюда. Впрочем, вон тот фиолетовый плод выглядит аппетитно._'
    counteat = 0
    countequip = 0
    countitem = 0
    shop = db.Shop.select().where(db.Shop.count>0)
    for counts in shop:
        if counts.type == 'Еда':
            counteat += 1
        elif counts.type == 'Экипировка' or counts.type == 'Зелье':
            countequip += 1
        elif counts.type == 'Броня':
            countitem += 1
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if counteat > 0:
        markup.add(InlineKeyboardButton('🍕 Пища', callback_data="shop_eat"))
    else:
        markup.add(InlineKeyboardButton('🍕 Пища (отсутствует в продаже)', callback_data="return"))
    if countequip > 0:
        markup.add(InlineKeyboardButton('🧢 Экипировка', callback_data="shop_equip"))
    else:
        markup.add(InlineKeyboardButton('🧢 Экипировка (отсутствует в продаже)', callback_data="return"))
    if countitem > 0:
        markup.add(InlineKeyboardButton('🛡 Броня', callback_data="shop_item"))
    else:
        markup.add(InlineKeyboardButton('🛡 Броня (отсутствует в продаже)', callback_data="return"))
    usr = db.Users.get(user_id=m1)
    if usr.location == 'Город':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
    elif usr.location == 'Хэвенбург':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
    gg = bot.edit_message_text(text, m1, m3, reply_markup=markup, parse_mode = 'markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('return'))
def ret(call): 
    return

@bot.callback_query_handler(func=lambda call: call.data.startswith('shop_'))
def _shop(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    armorOld = ['Кожаный шлем', 'Кожаный нагрудник', 'Кожаные штаны', 'Кожаные ботинки']
    sh = call.data.split('_')
    select = sh[1]
    user = db.Users.get(user_id=call.from_user.id)
    if select == 'close':
        user.position = 'Площадь'
        user.save()
        gg = bot.edit_message_text('Вы закрыли магазин.', call.message.chat.id, call.message.message_id)
        return
    elif select == 'eat':
        Type = 'Еда'
    elif select == 'equip':
        Type = 'Экипировка'
    elif select == 'item':
        Type = 'Броня'
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = "Выберите предмет для покупки: \n"
    shop = db.Shop.select().where(db.Shop.type==Type, db.Shop.count > 0)
    for item in shop:
        if Type == 'Броня' and user.location == 'Город' and item.name in armorOld:
            name, size, bonus = db.items(item.name, check=True)
            text += "\nx{} {} | {}💰".format(item.count, name, item.price)
            markup.add(InlineKeyboardButton('{}'.format(name), callback_data="buy_{}".format(item.id)))
        elif Type == 'Броня' and user.location == 'Хэвенбург':
            name, size, bonus = db.items(item.name, check=True)
            text += "\nx{} {} | {}💰".format(item.count, name, item.price)
            markup.add(InlineKeyboardButton('{}'.format(name), callback_data="buy_{}".format(item.id)))
        elif Type != 'Броня':
            name, size, bonus = db.items(item.name, check=True)
            text += "\nx{} {} | {}💰".format(item.count, name, item.price)
            markup.add(InlineKeyboardButton('{}'.format(name), callback_data="buy_{}".format(item.id)))
    markup.add(InlineKeyboardButton('↩️ Вернуться', callback_data="backtoshop"))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    sh = call.data.split('_')
    select = sh[1]
    item = db.Shop.get(id=select)
    if item.count <= 0:
        text = "К сожалению, товар кончился."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')
        return
    name, size, bonus = db.items(item.name, check=True)
    user = db.Users.get(user_id=call.from_user.id)
    if user.location == 'Город' or user.location == 'Хэвенбург':
        pass
    else:
        gg = bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)
        return
    if user.money >= item.price:
        if item.name == 'Улучшенный рюкзак':
            check = db.Inventory.get(idplayer=user.id, name='Улучшенный рюкзак')
            if check:
                text = "_Покупка дополнительного рюкзака не поможет тебе унести больше!_"
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')
                return
        success = db.addItem(item.name, user)
        db.specialItems(name, user)
        if success == True:
            item.count = item.count - 1
            item.save()
            user.money = user.money - item.price
            user.save()
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно приобретено: {}".format(item.name))                
            bot.send_message(tradeChat, "Игрок {} купил {} за {}💰".format(user.username, item.name, item.price))
            return
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нет места в рюкзаке")          
    else:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Недостаточно золота")                



@bot.callback_query_handler(func=lambda call: call.data.startswith('donateshop'))
def donateshop(call):
    user = db.Users.get(user_id=call.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('+5📦', callback_data="dshopbuy_1"), InlineKeyboardButton('+1000🍗', callback_data="dshopbuy_2"))
    markup.add(InlineKeyboardButton('Сменить группировку', callback_data="dshopbuy_3"))
    markup.add(InlineKeyboardButton('Сменить никнейм', callback_data="dshopbuy_4"))
    markup.add(InlineKeyboardButton('🏺Амфора экстренной помощи', callback_data="dshopbuy_5"))
    text = "Добро пожаловать в магазин 💎. Тут вы можете приобрести дополнительные бонусы.\nУ вас {}💎\n\n".format(user.almaz)
    text += "+5📦(25💎). Можно купить единоразово и расширить инвентарь на 5📦"
    text += "\n+1000🍗(5💎). Поможет вам не обращать внимания на проблемы с энергией и голодом. В случае смерти или использования еды - показатель сбивается"
    text += "\nСмена группировки(50💎). Позволяет выбрать новую группировку"
    text += "\nСмена никнейма(20💎). Вы можете сменить свой никнейм, если предыдущий вас не устраивает (или нет)"
    text += "\n🏺Амфора экстренной помощи(5💎). Позволяет в любом месте получить любую из трёх вещей на выбор (свиток телепортации, еда, зелье здоровья)"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dshopbuy_'))
def dshopbuy(call):
    sh = call.data.split('_')
    select = sh[1]
    user = db.Users.get(user_id=call.from_user.id)
    if select == '1':
        if user.almaz >= 25:
            if db.Inventory.get(name='Донат инв', idplayer=user.id):
                text = "Данный бонус можно купить лишь один раз."
            else:
                user.almaz -= 25
                item = db.Inventory(name='Донат инв', type='Донат', size=0, bonus=0, active=0, idplayer=user.id)
                item.save()
                user.inventorySizeMax += 5
                user.save()
                text = "Вы успешно приобрели +5📦"
        else:
            text = "У вас не хватает 💎"
    elif select == '2':
        if user.almaz >= 5:
            user.almaz -= 5
            user.eat += 1000
            user.save()
            text = "Вы успешно приобрели +1000🍗"
        else:
            text = "У вас не хватает 💎"
    elif select == '3':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 50:
            user.almaz -= 50
            user.save()
            text = "Вы успешно приобрели +1000🍗"
            markup.add(InlineKeyboardButton('🌋Грязное небо', callback_data="donateSelectGroup_1"))
            markup.add(InlineKeyboardButton('🗼Вавилон', callback_data="donateSelectGroup_2"))
            markup.add(InlineKeyboardButton('⚔️Небесные рыцари', callback_data="donateSelectGroup_3"))
            markup.add(InlineKeyboardButton('💠Хранители', callback_data="donateSelectGroup_4"))
        else:
            text = "У вас не хватает 💎"
    elif select == '4':
        if user.almaz >= 20:
            gg = bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            bot.register_next_step_handler(gg, reg_nick)
            text = "Начался процесс смены никнейма..."
            user.almaz -= 20
            user.save()
        else:
            text = "У вас не хватает 💎"
    elif select == '5':
        if user.almaz >= 5:
            user.almaz -= 5
            user.save()
            success = db.addItem('Амфора экстренной помощи', user)
            text = "Вы успешно приобрели 🏺Амфора экстренной помощи"
        else:
            text = "У вас не хватает 💎"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('donateSelectGroup_'))
def donateSelectGroup(call):
    sh = call.data.split('_')
    f = sh[1]
    user = db.Users.get(user_id=call.from_user.id)
    frak = db.Fraks.get(name=user.frak)
    frak.players -= 1
    frak.save()
    if user.frak == 'Хранители':
        bot.kick_chat_member(-1001320424099, m.from_user.id)
    elif user.frak == 'Небесные рыцари':
        bot.kick_chat_member(-1001467052649, m.from_user.id)
    elif user.frak == 'Грязное небо':
        bot.kick_chat_member(-1001121150202, m.from_user.id)
    elif user.frak == 'Вавилон':
        bot.kick_chat_member(-1001336335908, m.from_user.id)
    if f == '1':
        link = 'https://t.me/joinchat/Kd-6VBY61CSikVObkJdJJQ'
        user.frak = "Грязное небо"
        frak = db.Fraks.get(name=user.frak)
        frak.players += 1
    elif f == '2':
        link = 'https://t.me/joinchat/Kd-6VBY5L9HenYxFd_PSOw'
        user.frak = "Вавилон"
        frak = db.Fraks.get(name=user.frak)
        frak.players += 1
    elif f == '3':
        link = 'https://t.me/joinchat/Kd-6VFdxcmk2qB352-qD9A'
        user.frak = "Небесные рыцари"
        frak = db.Fraks.get(name=user.frak)
        frak.players += 1
    elif f == '4':
        link = 'https://t.me/joinchat/Kd-6VBmrXcTK0Lt9lMDmEg'
        user.frak = "Хранители"
        frak = db.Fraks.get(name=user.frak)
        frak.players += 1
    frak.save()
    user.save()


@bot.callback_query_handler(func=lambda call: call.data.startswith('shopsell'))
def shopsell(call):
    user = db.Users.get(user_id=call.from_user.id)
    if user.location == 'Хэвенбург' and user.position == 'Площадь':
        pass
    else:
        gg = bot.edit_message_text("Вы находитесь вне площади", call.message.chat.id, call.message.message_id)
        return
    inventory = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.active==1)
    text = "Выберите предмет на продажу:\n\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    passed = 0
    for item in inventory:
        checkShop = db.Shop.select().where(db.Shop.name==item.name).order_by(db.Shop.id.desc()).limit(1)
        if checkShop:
            for z in checkShop:
                price = int(z.price / 3)
                if z.name == 'Амулет здоровья' or z.name == 'Кольцо живости' or z.name == 'Осколок энергии':
                    price = 250
                name, size, bonus = db.items(item.name, check=True)
                text += "{} - {}💰\n".format(name, price)
                markup.add(InlineKeyboardButton('Продать {}'.format(name), callback_data="lombardsell_{}_{}".format(item.id, price)))
            passed = 1
    if passed == 0:
        text = "_Ну и что это ты мне принёс? Еще бы консервных банок насобирал! Мне такой хлам не нужен!_"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('backtoshop'))
def backtoshop(call):
    m1 = call.from_user.id
    m2 = call.message.chat.id
    m3 = call.message.message_id
    shop(m1, m2, m3)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lombardsell_'))
def lombardsell(call):
    sh = call.data.split('_')
    itemId = sh[1]
    item = db.Inventory.get(id=itemId)
    if item.active != 1:
        text = "Ошибка. Предмета не существует"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        return
    else:
        Type, size, bonus = db.items(item.name, check=False)
        user = db.Users.get(user_id=call.from_user.id)
        item.active = 0
        item.save()
        price = sh[2]
        pricesell = int(price) * 3
        user.money += int(price)
        user.save()
        checkInSell = db.Shop.select().where(db.Shop.name==item.name).order_by(db.Shop.count.desc()).limit(1)
        for z in checkInSell:
            z.count += 1
            z.save()
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы успешно продали {} за {}💰".format(item.name, price))                
        bot.send_message(tradeChat, "[ЛОМБАРД] Игрок {} продал {} за {}💰".format(user.username, item.name, price))
        inventory = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.active==1)
        text = "Выберите предмет на продажу:\n\n"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        passed = 0
        for item in inventory:
            checkShop = db.Shop.select().where(db.Shop.name==item.name).order_by(db.Shop.id.desc()).limit(1)
            if checkShop:
                for z in checkShop:
                    price = int(z.price / 3)
                    if z.name == 'Амулет здоровья' or z.name == 'Кольцо живости' or z.name == 'Осколок энергии':
                        price = 250
                    name, size, bonus = db.items(item.name, check=True)
                    text += "{} - {}💰\n".format(name, price)
                    markup.add(InlineKeyboardButton('Продать {}'.format(name), callback_data="lombardsell_{}_{}".format(item.id, price)))
                passed = 1
        if passed == 0:
            text = "Предметы кончились"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)


###############
#   СКУПЩИК   #
###############
@bot.callback_query_handler(func=lambda call: call.data.startswith('bomjsell'))
def bomjsell(call):
    user = db.Users.get(user_id=call.from_user.id)
    if user.location == 'Хэвенбург' and user.position == 'Площадь':
        pass
    else:
        gg = bot.edit_message_text("Вы находитесь вне площади", call.message.chat.id, call.message.message_id)
        return
    inventory = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.active==1, db.Inventory.type=='Хлам')
    text = "Выберите предмет на продажу:\n\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    passed = 0
    for item in inventory:
        if item.name == 'Перо ястреба':
            pass
        else:
            passed = 1
            name, size, bonus = db.items(item.name, check=True)
            text += "{}\n".format(name)
            markup.add(InlineKeyboardButton('Продать {}'.format(name), callback_data="bomj_sell_{}".format(item.id)))
    if passed == 0:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вам нечего предложить")                
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('bomj_sell_'))
def bomj_sell(call):
    sh = call.data.split('_')
    itemId = sh[2]
    item = db.Inventory.get(id=itemId)
    if item.active != 1:
        text = "Ошибка. Предмета не существует"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        return
    else:
        Type, size, bonus = db.items(item.name, check=False)
        user = db.Users.get(user_id=call.from_user.id)
        item.active = 0
        item.save()
        price = random.randint(20, 55)
        user.money += int(price)
        user.save()
        text = "Вы успешно продали {} за {}💰".format(item.name, price)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
        bot.send_message(tradeChat, "[СКУПЩИК] Игрок {} продал скупщику {} за {}💰".format(user.username, item.name, price))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)
