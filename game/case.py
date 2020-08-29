def case(item):
    rand = random.randint(1, 100)
    if item.name == 'Маленький сундучок':
        armorset = ['Хоккейная маска', 'Кожаный нагрудник', 'Кожаные штаны', 'Берцы']
        eat = ['Лучше не спрашивай', 'Большой хер огра']
        last = 'Туннельный свиток'
    elif item.name == 'Шкатулка Кефира':
        armorset = ['Шляпа фокусника', 'Комбинезон сталкера', 'Нижнее бельё Раскуловой', 'Кросы адидас']
        eat = ['Лучше не спрашивай', 'Большой хер огра']
        last = 'Детектор аномалий'
    elif item.name == 'Огромный сундук':
        armorset = ['Кепка адидас', 'Ночнушка Раскуловой', 'Штаны Ашодас', 'Туфельки Раскуловой']
        eat = ['Лучше не спрашивай', 'Большой хер огра']
        last = 'Отрицательный тест на беременность'
    elif item.name == 'Ashot case':
        armorset = ['Кожаный шлем', 'Бронежилет', 'Спортивки адидас', 'Кожаные ботинки']
        eat = ['Он называет это "яблоко"', 'Большой хер огра']
        last = 'Бесплатная путёвка на свалку'
    elif item.name == 'Амфора экстренной помощи':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Еда', callback_data="extraCase_eat"))
        markup.add(InlineKeyboardButton('Зелье здоровья', callback_data="extraCase_heal"))
        markup.add(InlineKeyboardButton('Свиток телепортации', callback_data="extraCase_tp"))
        text = "_Потерев эту штуковину, ты призвал джина, который предоставляет тебе три вещи на выбор совершенно бесплатно:_"
        user = db.Users.get(id=item.idplayer)
        bot.send_message(user.user_id, text, reply_markup=markup, parse_mode='markdown')
        text = "Потереть..."
        return text
    elif item.name == 'Аптечка':
        armorset = ['Колпак главврача', 'Халат главрача', 'Штаны главврача', 'Тапочки главврача']
        moneyBonus = random.randint(10, 35)
        user = db.Users.get(id=item.idplayer)
        user.money += moneyBonus
        user.save()
        armor = random.choice(armorset)
        success = db.addItem(armor, user)
        name, size, bonus = db.items(armor, check=True)
        if success == False:
            item.active = 1
            item.save()
            text = "У вас не хватает места в инвентаре. Открыть аптечку не получится."
            return text
        else:
            text = "*Распахнув сумку с красным крестом, ты обнаружил*\n{}".format(name)
        item.active = 0
        item.save()
        success = db.addItem('Успокаивающее', user)
        name, size, bonus = db.items('Успокаивающее', check=True)
        if success == False:
            item.active = 1
            item.save()
            text += "У вас не хватает места в инвентаре. Открыть аптечку не получится."
            return text
        else:
            text += "\n{}".format(name)
        text += "\n💰{}".format(moneyBonus)
        item.active = 0
        item.save()
        return text
    elif item.name == 'Сун-дук':
        user = db.Users.get(id=item.idplayer)
        armorset = ['Шлем из фольги', 'Майка из пакета', 'Модные штаны', 'НЕкроссовки']
        winnerItem = random.choice(armorset)
        success = db.addItem(winnerItem, user)
        name, size, bonus = db.items(winnerItem, check=True)
        if success == False:
            item.active = 1
            item.save()
            text = "У вас не хватает места в инвентаре. Открыть сун-дук не получится."
            return text
        else:
            text = "Вы открыли сун-дук. Внутри вы нашли {}".format(name)
        item.active = 0
        item.save()
        return text
    item.active = 0
    item.save()
    if rand <= 15:
        winnerItem = random.choice(armorset)
    elif rand > 15 and rand <= 30:
        winnerItem = random.choice(eat)
    elif rand > 30 and rand <= 40:
        winnerItem = last
    else:
        winnerItem = 'Ничего'
    user = db.Users.get(id=item.idplayer)
    text = "Применив самые современные приспособления по вскрытию этих таинственных сундуков, ты наконец распахнул этот кейс. Точнее, то что от него осталось после монотонного битья молотком."
    if winnerItem != 'Ничего':
        success = db.addItem(winnerItem, user)
        if success == False:
            item.active = 1
            item.save()
            text = "У вас не хватает места в инвентаре. Открыть сундук не получится."
            return text
        name, size, bonus = db.items(winnerItem, check=True)
        text += "\nВнутри сундука ты нашёл {}".format(name)
    else:
        text += "\nК сожалению, внутри ты ничего, полезного для себя, не обнаружил... Если тебе не нужны, конечно, останки от предыдущих ''героев'', что пошли на свалку."
    return text






@bot.callback_query_handler(func=lambda call: call.data.startswith('extraCase_'))
def extraCase(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    idp = db.Users.get(user_id=call.from_user.id)
    checkdonate = db.Inventory.get(name='Амфора экстренной помощи', active=1, idplayer=idp.id)
    if checkdonate:
        if use == 'tp':
            success = db.addItem('Свиток телепортации', idp)
        elif use == 'heal':
            success = db.addItem('Большое зелье здоровья', idp)
        elif use == 'eat':
            success = db.addItem('Лучше не спрашивай', idp)
        if success == True:
            text = "Ты сделал свой выбор\n_Джин послушно исполнил твою просьбу, а затем расстаял в воздухе вместе с амфорой. Рюкзак потяжелел_"
            checkdonate.active = 0
            checkdonate.save()
        else:
            text = "Для начала, тебе стоит освободить инвентарь. После можешь выбрать снова"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Еда', callback_data="extraCase_eat"))
            markup.add(InlineKeyboardButton('Зелье здоровья', callback_data="extraCase_heal"))
            markup.add(InlineKeyboardButton('Свиток телепортации', callback_data="extraCase_tp"))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
    else:
        text = "У вас уже нет амфоры"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')