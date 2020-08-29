def navigation(m):
    #tp[m.from_user.id] = 2
    user = db.Users.get(user_id=m.from_user.id)
    if user.location == "Город":
        if user.position == "Ворота":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Источники":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Магазин":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Отель":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Отдыхать в номере - 💰5', callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Номер в отеле":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Площадь":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_city_kachalka"))
            markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_city_trades"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        elif user.position == "Арена":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        else:
            bot.send_message(m.chat.id, "Не удалось установить местоположение. Обратитесь в /report")
        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)
    elif user.location == 'Большой город':
        return
    elif user.location == 'Хэвенбург':
        if user.position == "Ворота":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Источники":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Магазин":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Отель":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Отдыхать в номере - 💰5', callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Номер в отеле":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Площадь":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_bigcity_kachalka"))
            markup.add(InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_bigcity_raskul"))
            markup.add(InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard"))
            markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_bigcity_trades"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('👨🏾‍🦳Одинокий бомж', callback_data="nav_bigcity_skupshik"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Бар":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_bigcity_kachalka"))
            markup.add(InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_bigcity_raskul"))
            markup.add(InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard"))
            markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_bigcity_trades"))
            markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('👨🏾‍🦳Одинокий бомж', callback_data="nav_bigcity_skupshik"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        elif user.position == "Арена":
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
            markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
            markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
            markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        else:
            bot.send_message(m.chat.id, "Не удалось установить местоположение. Обратитесь в /report")
            return
        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)
    else:
        bot.send_message(m.chat.id, "📡Местоположение \n{}.📡\n\nНавигация в этой локации недоступна. Вы можете телепортироваться в город, используя телепорт в инвентаре.".format(str(user.location)))




@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_location_'))
def nav_location(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[2]
    user = db.Users.get(user_id=call.from_user.id)
    user.position = 'Площадь'
    user.save()
    if navWhere == "start":
        text = ""
        if user.location != "Город":
            gg = bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            return
        if user.questId == 0:
            quest = "«Время душить змей»"
            user.questId = 1
            user.quest = "«Время душить змей»"
            user.questStatus = 1
            user.save()
            text += "К вам подошёл охранник ворот и предложил заработать. Естественно, вы согласились\n\n'Эти шипящие шнурки меня вкрай достали, вся жопа в их укусах, скоро ампутировать придётся. Пойди-ка, истреби в округе этих тварей, пока мне её не ампутировали.'\n⚠️Получено задание: «Время душить змей»\nУсловия: Добыть 3 тушки питона\n"
        if user.nowhp > 1:
            inventorySize = db.getInventorySize(user)
            if inventorySize < user.inventorySizeMax and user.lvl == 1:
                types = "Свиток телепортации"
                if db.Inventory.get(idplayer=user.id, active=1, name=types):
                    text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: 'Очередной смертник или новый герой?''"
                else:
                    text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: ''Очередной смертник или новый герой?''\nПолучено: 📜свиток телепортации"
                    db.addItem('Свиток телепортации', user)
            else:
                text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: ''Очередной смертник или новый герой?''"
        else:
            text += "_Ну и куда ты собрался-то, ты едва на ногах стоишь! Вали отсюда, хых, герой_"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            return
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.progLoc == "Город|0":
            markup.add(InlineKeyboardButton('Исследовать пустыню', callback_data="nav_location_1"))
        else:
            markup.add(InlineKeyboardButton('Продолжить исследование', callback_data="nav_location_1"))
        if user.questId != 0:
            markup.add(InlineKeyboardButton('Подойти к охраннику', callback_data="nav_city_ohr"))
        markup.add(InlineKeyboardButton('Идти на свалку', callback_data="nav_location_svalka"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif navWhere == 'svalka':
        newLocation = "Свалка"
        if user.location == "Город":
            pass
        else:
            gg = bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            return
        user.location = newLocation
        user.progStatus = 1
        user.save()
        text = "Вы отправились на верную смерть - Свалка. Поздравляю!"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    else:
        result = db.Locations.get(id=1)
        if not result:
            text = "Ошибка определения отправления - не существует такой локации"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if user.progLoc == "Город|0":
            user.ProgLoc = "Пустыня|1".format(result.name)
            user.location = 'Пустыня'
            user.progStatus = 1
            user.save()
            text = "Вы успешно отправились исследовать локацию *{}*".format(result.name)
        else:
            if user.location == result.prev or user.location == "Город" or user.location == "Свалка" and result.name == "Пустыня":
                user.progLoc = "{}|1".format(result.name)
                user.location = result.name
                user.progStatus = 1
                user.save()
                text = "Вы успешно отправились исследовать локацию *{}*".format(str(result.name))
            else:
                text = "Сообщение устарело"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode= 'markdown')












@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_city_'))
def nav_city(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[2]
    user = db.Users.get(user_id=call.from_user.id)
    if navWhere == "onsen":
        newPos = "Источники"
        if (str(user.location) == "Город") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            if int(user.lvl <= 1):
                text = "_Пар нежно обволакивал голые тела молодых девиц, отдыхающих в этих божественных источниках. Как только они увидели тебя, сразу же поманили пальцем и указали на специально выделенное для тебя местечко в горячей воде между двумя не менее горячими дамами..._\n\n\nИменно так ты себе представлял горячие источники, пока не увидел кучу ржавых корыт соединённых одной сплошной трубой, проводящей желтоватую тёплую воду.\nИсцеление проходит постепенно, нужно немного подождать"
            else:
                text = "Ты снова пришёл в старое место, где увидел кучу ржавых корыт соединённых одной сплошной трубой, проводящей желтоватую тёплую воду.\nИсцеление проходит постепенно, нужно немного подождать"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            return
        elif str(user.location) != "Город":
            text = "Ты находишься вне города."
        elif int(user.hp) <= int(user.nowhp):
            text = "_Ну и на кой ты сюда с полным здоровьем припёрся? А ну брысь отсюда! И чтоб здоровым не возвращался!_"
        elif str(user.position) == newPos:
            text = "Ты уже находишься в горячих источниках.\nИсцеление проходит постепенно, нужно немного подождать"
        else:
            text = "Ошибка определителя. Location {} \n Hp/nowhp {}/{}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.nowhp), str(user.hp), str(user.position), str(newPos))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)
    elif navWhere == "hotel":
        newPos = "Отель"
        if (str(user.location) == "Город") and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Отдыхать в номере - 💰5', callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="hotel_return"))
            text = '_На ресепшене чуть ли не засыпает некий небритый мужик, зал пустой и всем своим видом показывающий, что уборщица сюда не заходила с момента постройки сего здания._ Мужик воскликнул: "КТО СПИТ? Я НЕ СПЛЮ! ПОДХОДИ, СПРАШИВАЙ, НЕ СТЕСНЯЙСЯ." и принялся делать вид, что он что-то делает.Чего тебе надобно, приятель?"'
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)
            return
        elif str(user.location) != "Город":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Город") and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            goToShop(call)
        elif str(user.location) != "Город":
            text = "Вы находитесь вне города"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        elif str(user.position) == newPos:
            text = "Вы уже в магазине."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            goToShop(call)
    elif navWhere == "centr":
        newPos = "Площадь"
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        newPos = "Площадь"
        user.position = newPos
        user.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_city_kachalka"))
        markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_city_trades"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
        markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        text = "Главная площадь - гордость этого города: кучка построек, начиная с качалки и заканчивая ларьком с мусором, в аккурат расставлены вокруг разбитого в труху фонтана с табличкой «Ремонт»"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "kachalka":
        atk = user.atk
        hp = user.hp
        needAtk = int(3 * ((atk - 4) / 2))
        needHp = int(3 * ((hp - 9) / 2))
        text = "Штанги из палок и покрышек, тренажёры из палок и покрышек, дверь в здание из палок и покрышек... Да чего уж таить — само здание тоже из палок и покрышек. Разве что табличка «Самые современные и технологичные тренажёры на любой вкус и цвет!» сделана не из покрышек\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰\n⚠️Акция от качалки - кто больше всего прокачается за неделю - получит +20❤️ и +20💢".format(str(needAtk), str(needHp))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(needAtk), callback_data="kach_atk"))
        markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(needHp), callback_data="kach_hp"))
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_city_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "trades":
        location = "Город"
        position = "Площадь"
        if user.location == location and user.position == position or user.location == 'Хэвенбург' and user.position == position:
            pass
        else:
            text = "Вы находитесь не на площади."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if user.lvl < 5:
            text = "Трейды доступны с 5 уровня."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        else:
            pass
        result = db.Users.select().where(db.Users.location==location, db.Users.position==position, db.Users.user_id != call.from_user.id)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for dict in result:
            markup.add(InlineKeyboardButton('{}'.format(dict.username), callback_data="trade_{}".format(dict.id)))
        text = "Выберите игрока, с которым хотите обменяться."
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif navWhere == "ohr":
        if user.questId == 1 and user.questStatus == 1:
            name = "Тушка питона"
            res = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.name==name, db.Inventory.active==1)
            if res:
                count = 0
                for dict in res:
                    count += 1
                if count >= 3:
                    q = db.Inventory.update(active=0).where(db.Inventory.name==name, db.Inventory.idplayer==user.id)
                    q.execute()
                    user.money = user.money + 40
                    user.questStatus = 0
                    user.save()
                    text = "Подойдя к охраннику, протягиваете ему скользские и противные тушки питонов. Он удовлетворённо кивнул и дал вам 40💰.\n'Заходи иногда, еще работёнки подкину, если есть желание.'"
                    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                    return
                else:
                    text = "Подойдя к охраннику, он фыркнул:\n'Так и думал, что ты - самая натуральная зелень, которая ни на что не способна... Проваливай отсюда'"
                    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                    return
            else:
                text = "Подойдя к охраннику, он фыркнул:\n'Так и думал, что ты - самая натуральная зелень, которая ни на что не способна... Проваливай отсюда'"
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
        elif user.questId == 1 and user.questStatus == 0:
            quest = "«Выдиратель хвостов»"
            user.questId = 2
            user.quest = quest
            user.questStatus = 1
            user.save()
            text = "Подходя к охраннику, тот с радостью приобнял вас и начал просить вас насобирать 25 хвостов ястребов\n-Я хочу себе сшить новую подушку, но, как видишь, у меня почти не бывает выходных, чтобы выбраться наружу и собрать хвосты. Я тебе очень щедро заплачу, только сделай, пожалуйста, как надо...\n\n⚠️Получено задание: «Выдиратель хвостов»\nУсловия: Добыть 25 перьев ястребов.\n"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        elif user.questId == 2 and user.questStatus == 1:
            name = "Перо ястреба"
            res = db.Inventory.select().where(db.Inventory.idplayer==user.id, db.Inventory.name==name, db.Inventory.active==1)
            if res:
                count = 0
                for dict in res:
                    count += 1
                if count >= 25:
                    q = db.Inventory.update(active=0).where(db.Inventory.name==name, db.Inventory.idplayer==user.id)
                    q.execute()
                    user.money = user.money + 150
                    user.questStatus = 0
                    user.save()
                    text = "Подойдя к охраннику, достаёте мешок с перьями. Он кинулся вас целовать, но вы мягко его отодвинули, попросив оплату. Кивнул, он дал вам 150💰.\n'Я твой должник, спасибо тебе, родной!'"
                    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                    return
                else:
                    text = "Подойдя к охраннику, он покачал головой:\n'Боюсь, еще мало... Принеси побольше!'"
                    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                    return
            else:
                text = "Подойдя к охраннику, он покачал головой:\n'Боюсь, еще мало... Принеси побольше!'"
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
        else:
            text = "Подойдя к охраннику, тот покачал головой: \n'Боюсь, работы пока нет.'"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Купить 💎', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_city_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return




@bot.callback_query_handler(func=lambda call: call.data.startswith('kach_'))
def kach(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    user = db.Users.get(user_id=call.from_user.id)
    if kach == 'atk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if (user.money - needAtk) >= 0:
            user.atk = user.atk + 1
            user.money = user.money - needAtk
            user.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            text = "💢Атака: улучшено до {} за {}💰\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(atk), str(needAtk), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="kach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="kach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
            f = open('1.txt', 'a')
            f.write("\n{}".format(call.from_user.id))
            f.close()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            text = "Вам не хватает денег."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif kach == 'hp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if (user.money - needHp) >= 0:
            user.hp = user.hp + 1
            user.nowhp = user.nowhp + 1
            user.money = user.money - needHp
            user.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            text = "❤️Здоровье: улучшено до {} за {}💰\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(needHp), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="kach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="kach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
            f = open('1.txt', 'a')
            f.write("\n{}".format(call.from_user.id))
            f.close()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            text = "Вам не хватает денег."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)




#HOTEL
@bot.callback_query_handler(func=lambda call: call.data.startswith('hotel_'))
def hotel(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    hotel = call.data.split('_')
    hotelDo = hotel[1]
    user = db.Users.get(user_id=call.from_user.id)
    if hotelDo == "start":
        newPos = "Номер в отеле"
        if (str(user.position) == "Отель") and (int(user.money) >= 5):
            user.money = user.money - 5
            user.position = newPos
            user.save()
            text = "_Дяденька взял плату и метнул в тебя уже немного проржавевший ключ._\nЗайдя в свой номер, ты решил отдохнуть..."
        elif str(user.position) != "Отель":
            text = "Ты находишься вне отеля."
        elif int(user.money) < 5:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="У тебя нет денег") 
            return               
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\nMoney {}\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos), str(user.money))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Отдыхать в номере - 💰5', callback_data="hotel_start"))
        markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        gg = bot.edit_message_text("Вы находитесь в отеле города. Доступные варианты навигации:", call.message.chat.id, call.message.message_id, reply_markup=markup)







def goToShop(call): 
    name = 'shop_work'
    result = db.System.get(name=name)
    user = db.Users.get(user_id=call.from_user.id)
    if int(result.value) == 1:
        text = "_Ты подходишь к невзрачному стеллажу с выцвевшим навесом. Ощущение, словно владелец бросает сюда весь мусор, который только находит на близлежащей свалке. Впрочем, некоторые товары кажутся почти новыми._"
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    else:
        text = '_Вы подошли к магазину где стоял одинокий Ашот. \n-Эй, Ашотик, брат, продай мне чё-нибудь\n-Пашёль нахуй_'
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        return
    m1 = call.from_user.id
    m2 = call.message.chat.id
    m3 = call.message.message_id
    if user.lvl != 1:
        shop(m1, m2, m3)
    else:
        t = Timer(5, shop, [m1, m2, m3])
        t.start()

        ############
        #  TRADES  #
        ############

@bot.callback_query_handler(func=lambda call: call.data.startswith('trade_'))
def trade(call): 
    tr = call.data.split('_')
    tradeWith = tr[1]
    location = "Город"
    position = "Площадь"
    result = db.Users.get(user_id=call.from_user.id)
    usr = db.Users.get(user_id=call.from_user.id)
    idplayer = result.id
    if result.location == location and result.position == position or result.location == 'Хэвенбург' and result.position == position:
        pass
    else:
        text = "Вы находитесь не на площади."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    res = db.Users.get(id=tradeWith)
    if res.location == result.location and res.position == result.position:
        pass
    else:
        text = "Игрок находится вне площади."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    result = db.Inventory.select().where(db.Inventory.active==1, db.Inventory.idplayer==idplayer)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = "Выбери предмет для обмена с игроком *{}*\n\n⭐️Уровень доверия игрока: {}/5 \nОн совершил {} обменов.".format(res.username, res.tradenum, res.tradecount)
    for dict in result:
        if dict.name == "Тушка питона" or dict.name == "Перо ястреба":
            pass
        else:
            name, size, bonus = db.items(dict.name, check=True)
            markup.add(InlineKeyboardButton('{}'.format(name), callback_data="tradewith_{}_{}".format(tradeWith, dict.id)))
    if usr.location == 'Хэвенбург':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
    elif usr.location == 'Город':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('tradewith_'))
def tradewith(call): 
    if (call.from_user.id == call.from_user.id):
        pass
    else:
        return
    tr = call.data.split('_')
    tradeWith = tr[1]
    tradeItem = tr[2]
    location = "Город"
    position = "Площадь"
    result = db.Users.get(user_id=call.from_user.id)
    if result.location == location and result.position == position or result.location == 'Хэвенбург' and result.position == position:
        pass
    else:
        text = "Вы находитесь не на площади."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    res = db.Users.get(id=tradeWith)
    tradeWithId = res.user_id
    if res.location == result.location and res.position == result.position:
        pass
    else:
        text = "Игрок находится вне площади."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    item = db.Inventory.get(id=tradeItem)
    if item.active == 0:
        text = "Предмет отсутствует в вашем инвентаре."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    newTrade = db.Trades(fromP=result.id, toP=tradeWith, item=tradeItem, status=2)
    newTrade.save()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Принять', callback_data="trades_confirmfirst_{}".format(newTrade.id)))
    markup.add(InlineKeyboardButton('Отклонить', callback_data="trades_cancel_{}".format(newTrade.id)))
    markup.add(InlineKeyboardButton('Изменить трейд', callback_data="trades_edit_{}".format(newTrade.id)))
    try:
        name, size, bonus = db.items(item.name, check=True)
        bot.send_message(tradeWithId, "*Новое предложение обмена*\n\n Игрок *{}* предлагает:\n{}\n\nВыберите действие.".format(result.username, name), reply_markup=markup, parse_mode = 'markdown')
        text = "✅ Предложение на обмен #{} успешно отправлено \n{}➡️{}\n\nОжидайте решения второй стороны.".format(newTrade.id, item.name, res.username)
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    except:
        res.position = "Номер в отеле"
        text = "Игрок заблокировал бота. Трейд отменён."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        res.save()

@bot.callback_query_handler(func=lambda call: call.data.startswith('trades_'))
def trading(call): 
    st = call.data.split('_')
    do = st[1]
    tradeid = st[2]
    if do == 'confirm':
        trade = db.Trades.get(id=tradeid)
        trade.status = 3
        trade.save()
        item = db.Inventory.get(id=trade.item)
        itemreturn = db.Inventory.get(id=trade.itemreturn)
        fromP = db.Users.get(id=trade.fromP)
        toP = db.Users.get(id=trade.toP)
        text = "*Обмен #{} принят*. \n\nОжидание подтверждения второго пользователя.".format(trade.id)
        bot.send_message(toP.user_id, "Обмен #{}\nВы отдаёте: {}\nВы получаете: {}\nПодтвердить обмен /trade_accept_{}\nОтклонить обмен /trade_cancel_{}".format(trade.id, item.name, itemreturn.name, trade.id, trade.id))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif do == 'cancel':
        player1 = db.Users.get(user_id=call.from_user.id)
        text = "Вы отклонили обмен."
        trade = db.Trades.get(id=tradeid)
        trade.status = 0
        trade.save()
        if trade.itemreturn != None:
            player2 = db.Users.get(id=trade.toP)
            bot.send_message(player2.user_id, "Обмен #{} был отклонён".format(trade.id))
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            player2 = db.Users.get(id=trade.fromP)
            bot.send_message(player2.user_id, "Обмен #{} был отклонён".format(trade.id), parse_mode = 'markdown')
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif do == 'edit':
        player = db.Users.get(user_id=call.from_user.id)
        result = db.Trades.get(id=tradeid)
        res = db.Users.get(id=result.fromP)
        inv = db.Inventory.select().where(db.Inventory.idplayer==player.id, db.Inventory.active==1)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        text = "Выберите, что хотите предложить игроку {} взамен\nУровень доверия игрока - {}/5 , он совершил {} обменов.".format(res.username, res.tradenum, res.tradecount)
        for dict in inv:
            if dict.name == "Тушка питона":
                pass
            else:
                name, size, bonus = db.items(dict.name, check=True)
                markup.add(InlineKeyboardButton('{}'.format(name), callback_data="tradecon_{}_{}".format(tradeid, dict.id)))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')
    elif do == 'confirmfirst':
        result = db.Trades.get(id=tradeid)
        player1 = db.Inventory.get(id=result.item)
        player1user = db.Users.get(id=player1.idplayer)
        if player1.active == 1 and player1.idplayer == result.fromP:
            player1.idplayer = result.toP
            text = "Обмен завершен."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            player2 = db.Users.get(id=result.toP)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1', callback_data="tradestar_2_{}_1".format(tradeid)))
            markup.add(InlineKeyboardButton('2', callback_data="tradestar_2_{}_2".format(tradeid)))
            markup.add(InlineKeyboardButton('3', callback_data="tradestar_2_{}_3".format(tradeid)))
            markup.add(InlineKeyboardButton('4', callback_data="tradestar_2_{}_4".format(tradeid)))
            markup.add(InlineKeyboardButton('5', callback_data="tradestar_2_{}_5".format(tradeid)))
            bot.send_message(player1user.user_id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup)
            result.status = 1
            tradeResult = db.Trades.get(id=tradeid)
            _fromP = db.Users.get(id=tradeResult.fromP)
            fromP = _fromP.username
            _toP = db.Users.get(id=tradeResult.toP)
            toP = _toP.username
            player1user.tradecount += 1
            player1user.save()
            _toP.tradecount += 1
            _toP.save()
            itemresult = db.Inventory.get(id=tradeResult.item)
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{}\nПредмет: {}".format(tradeResult.id, fromP , toP, itemresult.name))
        else:
            text = "Какого-то предмета уже не существует. Обмен отклонён"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            result.status = 0
        result.save()
        player1.save()
        player1user.save()



@bot.callback_query_handler(func=lambda call: call.data.startswith('tradecon_'))
def tradecon(call): 
    tr = call.data.split('_')
    tradeid = tr[1]
    tradeItem = tr[2]
    location = "Город"
    position = "Площадь"
    r = db.Trades.get(id=tradeid)
    tradeWith = r.fromP
    nameitem = db.Inventory.get(id=r.item)
    r.itemreturn = tradeItem
    r.save()
    result = db.Users.get(id=r.toP)
    res = db.Users.get(id=tradeWith)
    tradeWithId = res.user_id
    item = db.Inventory.get(id=tradeItem)
    if item.active == 0:
        text = "Предмет отсутствует в вашем инвентаре."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Принять', callback_data="trades_confirm_{}".format(tradeid)))
    markup.add(InlineKeyboardButton('Отклонить', callback_data="trades_cancel_{}".format(tradeid)))
    name, size, bonus = db.items(item.name, check=True)
    returnname, returnsize, returnbonus = db.items(nameitem.name, check=True)
    bot.send_message(tradeWithId, "*{}* отправил встречное предложение обмена #{}: \n\nЕго {} взамен на ваше {}\n\nВыберите действие.".format(result.username, r.id, name, returnname), reply_markup=markup, parse_mode = 'markdown')
    text = "✅ Встречное предложение успешно отправлено \n{}➡️{}\nОжидайте решения второй стороны.".format(name, res.username)
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')


@bot.message_handler(func=lambda m:m.text and m.text.startswith('/trade_accept_'))
def tradeaccept(m):
    tradeid = m.text.replace('/trade_accept_', '', 1).replace('@MeguNext_bot', '', 1)
    result = db.Trades.get(id=tradeid)
    if result.itemreturn == None:
        result.itemreturn = 0
    player1 = db.Inventory.get(id=result.item)
    player1user = db.Users.get(id=player1.idplayer)
    if player1user.location == 'Хэвенбург' or player1user.location == 'Город':
        pass
    else:
        bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    player2 = db.Users.get(id=result.fromP)
    if player2 and player2.location == 'Хэвенбург' or player2 and player2.location == 'Город':
        pass
    else:
        bot.send_message(m.chat.id, "Игрок находится вне города")
        return
    if result.itemreturn == 0:
        def player2(result):
            idplayer = result.toP
            active = 1
        player2(result)
    else:
        player2 = db.Inventory.get(id=result.itemreturn)
    if player1.active == 1 and player1.idplayer == result.fromP:
        if player2.active == 1 and player2.idplayer == result.toP:
            inv1 = db.Inventory.get(id=result.item)
            inv1.idplayer = result.toP
            inv1.save()
            if result.itemreturn == 0:
                pass
            else:
                inv2 = db.Inventory.get(id=result.itemreturn)
                inv2.idplayer = result.fromP
                inv2.save()
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1', callback_data="tradestar_1_{}_1".format(tradeid)))
            markup.add(InlineKeyboardButton('2', callback_data="tradestar_1_{}_2".format(tradeid)))
            markup.add(InlineKeyboardButton('3', callback_data="tradestar_1_{}_3".format(tradeid)))
            markup.add(InlineKeyboardButton('4', callback_data="tradestar_1_{}_4".format(tradeid)))
            markup.add(InlineKeyboardButton('5', callback_data="tradestar_1_{}_5".format(tradeid)))
            bot.send_message(m.chat.id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup)
            player2 = db.Users.get(id=result.fromP)
            markup2 = InlineKeyboardMarkup()
            markup.row_width = 2
            markup2.add(InlineKeyboardButton('1', callback_data="tradestar_2_{}_1".format(tradeid)))
            markup2.add(InlineKeyboardButton('2', callback_data="tradestar_2_{}_2".format(tradeid)))
            markup2.add(InlineKeyboardButton('3', callback_data="tradestar_2_{}_3".format(tradeid)))
            markup2.add(InlineKeyboardButton('4', callback_data="tradestar_2_{}_4".format(tradeid)))
            markup2.add(InlineKeyboardButton('5', callback_data="tradestar_2_{}_5".format(tradeid)))
            bot.send_message(player2.user_id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup2)
            tradeResult = db.Trades.get(id=tradeid)
            _fromP = db.Users.get(id=tradeResult.fromP)
            _toP = db.Users.get(id=tradeResult.toP)
            fromP = _fromP.username
            toP = _toP.username
            _fromP.tradecount += 1
            _toP.tradecount += 1
            _fromP.save()
            _toP.save()
            __item = db.Inventory.get(id=tradeResult.item)
            __itemret = db.Inventory.get(id=tradeResult.itemreturn)
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{}\nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, __item.name, __itemret.name))
            tradeResult.status = 1
            tradeResult.save()
        else:
            trade = db.Trades.get(id=tradeid)
            trade.status = 0
            trade.save()
            bot.send_message(m.chat.id, "Какого-то предмета уже не существует. Обмен отклонён")
    else:
        result.status = 0
        result.save()
        bot.send_message(m.chat.id, "Какого-то предмета уже не существует. Обмен отклонён")



@bot.callback_query_handler(func=lambda call: call.data.startswith('tradestar_'))
def tradestar(call): 
    st = call.data.split('_')
    p = st[1]
    trade = st[2]
    star = st[3]
    if p == "1":
        tradeResult = db.Trades.get(id=trade)
        tradeResult.star = star
        tradeResult.save()
        _fromP = db.Users.get(id=tradeResult.fromP)
        fromP = _fromP.username
        _toP = db.Users.get(id=tradeResult.toP)
        toP = _toP.username
        text = "Оценка отправлена."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        __item = db.Inventory.get(id=tradeResult.item)
        try:
            __itemret = db.Inventory.get(id=tradeResult.itemreturn)
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, star, toP, __item.name, __itemret.name))
        except:
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}".format(tradeResult.id, fromP , toP, star, toP, __item.name))
    elif p == "2":
        tradeResult = db.Trades.get(id=trade)
        tradeResult.star2 = star
        tradeResult.save()
        _fromP = db.Users.get(id=tradeResult.fromP)
        _toP = db.Users.get(id=tradeResult.toP)
        fromP = _fromP.username
        toP = _toP.username
        text = "Оценка отправлена."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        __item = db.Inventory.get(id=tradeResult.item)
        try:
            __itemret = db.Inventory.get(id=tradeResult.itemreturn)
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, star, fromP, __item.name, __itemret.name))
        except:
            bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}".format(tradeResult.id, fromP , toP, star, fromP, __item.name))

