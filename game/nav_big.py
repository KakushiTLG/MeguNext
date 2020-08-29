
@bot.callback_query_handler(func=lambda call: call.data.startswith('startstartBigCity'))
def startstartCity(call):
    user = db.Users.get(user_id=call.from_user.id)
    item = db.Inventory(name='Большой город', type='Большой город', size=0, bonus=0, active=0, idplayer=user.id)
    item.save()
    text = 'Попинав здешнего спящего бомжа, ты убедился в том что этот город — не глюк. Вонь от бомжа, кстати, тоже вполне реальная'
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    chat = call.message.chat.id
    startBigCity(chat)

def startBigCity(chat):
    text = "–__Чё происходит... Ты какого хера творишь?! Аа, видать будил меня, чтобы выпивкой угостить, ну конечно же! Не стесняйся, пойдём, я знаю отличный бар здесь рядом.\n\nСкажу по секрету — он здесь единственный, так что выбирать не приходится.__\n\nОн, обняв тебя одной рукой, потащил в известном ему направлении..."
    photo = open('/home/kakushigoto/megu/media/bomj.jpg', 'rb')
    bot.send_photo(chat, photo, caption=text, parse_mode='markdown')
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Где мы находимся?', callback_data="startBigCity_1"))
    bot.send_message(chat, "Чёт незнакома мне твоя физиономия, да и пинаешь ты слабовато по сравнению с местными. Надо думать, ты с той безымянной деревни, висящей на соплях, которую почему-то все ещё называют городом. Наверное, в память о былых временах.\n\nИ так, раз уж я пью тут за твой счёт, могу рассказать все чего твоя душа пожелает. Будь уверен, лучшего специалиста в области всего тут нет. Что тебя интересует?", parse_mode='markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('startBigCity_'))
def startBigCity_ans(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    quest = call.data.split('_')
    q = quest[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = call.message.text
    if q == '1':
        markup.add(InlineKeyboardButton('Расскажи немного о городе', callback_data="startBigCity_2"))
        text = "\n''Что это за место?''\n_В столице нашей страны... Вернее того, что от неё осталось. Тут эдакие ''мирные воды'' на которых представители всех четырёх группировок могут отдохнуть  от сражений, ненависти и матюков._"
    elif q == '2':
        markup.add(InlineKeyboardButton('Есть ли организации, в которые я могу вступить?', callback_data="startBigCity_3"))
        text += "\n\n''Группировки?''\n_Мда, как всё запущено. Ладно, если вкратце: это разобщенные кучки народу, которые сражается за своё благополучие. Давай дальше._"
    elif q == '3':
        markup.add(InlineKeyboardButton('Расскажи о небесной башне', callback_data="startBigCity_4"))
        text += "\n\n''Есть ли организации, в которые я могу вступить?''\n_Да, ты можешь вступить в какую-нибудь группировку и помогать ей разузнать больше про небесную башню. _"
    elif q == '4':
        markup.add(InlineKeyboardButton('Как заработать?', callback_data="startBigCity_5"))
        text += "\n\n''Башня?''\n_Ну, это легенда, о которой знать должен каждый! Ты вообще откуда взялся, раз не знаешь, что это?.. Ох, ладно. В общем, легенда гласит о том, что это башня, которая простирается в самое небо и, пройдя до самого верха, ты можешь увидеть весь наш мир, найти... эээ... древние свитки, в которых описано наше прошлое, и поговаривают, в них есть карта, которая приведёт тебя к драгоценностям, о которых ты даже и не мечтал..."
        text += "Вот поэтому все и цапаются между собой за право владеть башней. Хотя до сих пор никто внутри ничего так и не нашёл..._"
    elif q == '5':
        markup.add(InlineKeyboardButton('Окей, как попасть в эти твои "группировки"?', callback_data="startBigCity_6"))
        text += "\n\n''Как заработать?''\n_А как ты до этого себе на жизнь зарабатывал? Я смотрю, броня у тебя не так уж и плоха, оружие при себе есть, да и сам ты выглядишь не слабым._"
    elif q == '6':
        fraks = db.Fraks.select().order_by(db.Fraks.players.desc()).limit(5)
        count = 0
        fr = {'Грязное небо': '1', 'Вавилон': '2', 'Небесные рыцари': '3', 'Хранители': '4'}
        f = {'Грязное небо': '🌋Грязное небо', 'Вавилон': '🗼Вавилон', 'Небесные рыцари': '⚔️Небесные рыцари', 'Хранители': '💠Хранители'}
        for x in fraks:
            count += 2
            markup.add(InlineKeyboardButton('{} (+{}💎)'.format(f[x.name], count), callback_data="startBigCity_7_{}".format(fr[x.name])))
        text += "\n\n''Окей, как попасть в эти твои ''группировки''? ''\n_Ты точно хочешь выбрать группировку? Впрочем, какая разница. МУЖИКИ, ЗДЕСЬ НУЖНО ГРУППИРОВКУ ВЫБРАТЬ, ЕСЛИ ВЫ ПОНИМАЕТЕ О ЧЁМ Я!..''_\n\n\n"
    elif q == '7':
        user = db.Users.get(user_id=call.from_user.id)
        f = quest[2]
        fraks = db.Fraks.select().order_by(db.Fraks.players.desc()).limit(5)
        count = 0
        fbonus = {}
        for x in fraks:
            count += 2
            fbonus[x.name] = count
        if f == '1':
            link = 'https://t.me/joinchat/Kd-6VBY61CSikVObkJdJJQ'
            user.frak = "Грязное небо"
            user.almaz += fbonus[user.frak]
            frak = db.Fraks.get(name=user.frak)
            frak.players += 1
        elif f == '2':
            link = 'https://t.me/joinchat/Kd-6VBY5L9HenYxFd_PSOw'
            user.frak = "Вавилон"
            user.almaz += fbonus[user.frak]
            frak = db.Fraks.get(name=user.frak)
            frak.players += 1
        elif f == '3':
            link = 'https://t.me/joinchat/Kd-6VFdxcmk2qB352-qD9A'
            user.frak = "Небесные рыцари"
            user.almaz += fbonus[user.frak]
            frak = db.Fraks.get(name=user.frak)
            frak.players += 1
        elif f == '4':
            link = 'https://t.me/joinchat/Kd-6VBmrXcTK0Lt9lMDmEg'
            user.frak = "Хранители"
            user.almaz += fbonus[user.frak]
            frak = db.Fraks.get(name=user.frak)
            frak.players += 1
        frak.save()
        minusmoney = user.money
        user.money = 0
        user.position = 'Площадь'
        user.location = 'Хэвенбург'
        user.save()
        leader = db.Users.get(id=frak.leader)
        try:
            bot.send_message(leader.user_id, "Новый игрок в группировке!\n{} - {}".format(user.username, call.from_user.username))
        except:
            pass
        text += "\n\n\nПосле внезапного удара по голове, все дальше было как в тумане. Ты проснулся спустя несколько часов с болью на левом жопном полушарии и без гроша в кармане. На вопрос о том, что случилось, бармен отвечал только то, что ты угощал всех выпивкой и тебе поставили клеймо выбранной группировки на... Думаю ты догадываешься на что.\n\nПотрачено {}💰\n\n\nНа заднице, помимо названия группировки, удобно выбита ссылка-приглашение на чат {}".format(minusmoney, link)
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')



@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_bigcity_'))
def nav_bigcity(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[2]
    user = db.Users.get(user_id=call.from_user.id)
    if navWhere == "onsen":
        newPos = "Источники"
        if (str(user.location) == "Хэвенбург") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Хэвенбург":
            text = "Ты находишься вне города."
        elif int(user.hp) <= int(user.nowhp):
            text = "_Послушай... Источники нужны для того, чтобы исцеляться, а не приходить сюда каждый раз только если бабу охота!_"
        elif str(user.position) == newPos:
            text = "Ты занимаешься *CENSORED*\nИсцеление проходит постепенно, нужно немного подождать"
        else:
            text = "Ошибка определителя. Location {} \n Hp/nowhp {}/{}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением в /report".format(str(user.location), str(user.nowhp), str(user.hp), str(user.position), str(newPos))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif navWhere == "hotel":
        newPos = "Отель"
        if (str(user.location) == "Хэвенбург") and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Пойти в номер (5 золотых)', callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('Уйти', callback_data="hotel_return"))
            text = '_«Отель» он же бывший бордель, закрытый из-за нехватки работниц, конечно, выглядит лучше после смены владельца и ремонта, однако  запах его прошлой жизни останется здесь ещё надолго_'
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)
            return
        elif str(user.location) != "Хэвенбург":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Хэвенбург") and (str(user.position) != newPos):
            user.position = newPos
            user.save()
            goToShop(call)
        elif str(user.location) != "Хэвенбург":
            text = "Ты находитесь вне города"
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        elif str(user.position) == newPos:
            text = "Ты уже в магазине."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            goToShop(call)
    elif navWhere == "centr":
        newPos = "Площадь"
        if user.location == "Хэвенбург":
            pass
        else:
            text = "Ты находитесь вне города."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        newPos = "Площадь"
        user.position = newPos
        user.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_bigcity_kachalka"))
        markup.add(InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard"))
        markup.add(InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_bigcity_raskul"))
        markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_bigcity_trades"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"))
        markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_bigcity_shop"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"))
        markup.add(InlineKeyboardButton('👨🏾‍🦳Одинокий бомж', callback_data="nav_bigcity_skupshik"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        text = "Площадь как площадь. Ведь площадь она и в Хэвенбурге площадь, верно? Знаешь как выглядят площади, так вот наша площадь практически такая же, как и все площади, что ты видел до неё. В общем, площадь, которая выглядит как площадь — вот она, наша площадь Хэвенбурга."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Случайный лес"
                if user.location == "Хэвенбург":
                    pass
                else:
                    gg = bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
                    return
                user.location = newLocation
                user.progStatus = 1
                user.progLoc = 'Случайный лес|0'
                user.save()
                text = "Вы отправились в Случайный лес"
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
            elif navg == 'tower':
                newLocation = "Тропа к башне"
                if user.location == "Хэвенбург":
                    pass
                else:
                    gg = bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
                    return
                user.location = newLocation
                user.progStatus = 1
                user.progLoc = 'Тропа к башне|0'
                user.save()
                text = "Вы отправились к Небесной башне"
                gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
            else:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Случайный лес', callback_data="nav_bigcity_exit_1"))
                markup.add(InlineKeyboardButton('Идти к башне', callback_data="nav_bigcity_exit_tower"))
                gg = bot.edit_message_text("Выберите, куда хотите пойти:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Случайный лес', callback_data="nav_bigcity_exit_1"))
            markup.add(InlineKeyboardButton('Идти к башне', callback_data="nav_bigcity_exit_tower"))
            gg = bot.edit_message_text("Выберите, куда хотите пойти:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "kachalka":
        if user.lvl == 1:
            text = "Качалка доступна со второго уровня."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        else:
            atk = user.atk
            hp = user.hp
            needAtk = int(3 * ((atk - 4) / 2))
            needHp = int(3 * ((hp - 9) / 2))
            text = "Штанги из палок и покрышек, тренажёры из палок и покрышек, дверь в здание из палок и покрышек... Да чего уж таить — само здание тоже из палок и покрышек. Разве что табличка «Самые современные и технологичные тренажёры на любой вкус и цвет!» сделана не из покрышек\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰\n⚠️Акция от качалки - кто больше всего прокачается за неделю - получит +20❤️ и +20💢".format(str(needAtk), str(needHp))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(needAtk), callback_data="bigkach_atk"))
        markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(needHp), callback_data="bigkach_hp"))
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_bigcity_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "trades":
        location = "Хэвенбург"
        position = "Площадь"
        if user.location == location and user.position == position:
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
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Купить 💎', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif navWhere == "skupshik":
        text = "Стоит, значит, возле фонтана солидного вида бомж, к которому подойти не страшно. Поманив тебя пальцем, пытается купить у тебя всякий редкий хлам."
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Идти к бомжу', callback_data="bomjsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif navWhere == "raskul":
        if user.lvl < 7:
            text = "Горячая дама принимает к себе только посетителей выше 7 уровня."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        else:
            pass
        if user.location != "Хэвенбург":
            text = "Ты находишься не в городе."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
        location = "Хэвенбург"
        position = "Арена"
        if user.nowhp < user.hp:
            text = "Подойдя к скучающей даме, она глянула на тебя и презрительно сказала, что с хлюпиками, которые едва на ногах стоят, она не играет."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        elif user.money < 35:
            text = "Подойдя к скучающей даме, она глянула на тебя и попросила оплату вперёд в размере 35💰. К сожалению, денег у тебя не нашлось."
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            user.position = position
            user.money = user.money - 35
            user.save()
            player = call.from_user.id
            pvpcheck(player, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bigkach_'))
def bigkach(call): 
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
        if user.location == "Хэвенбург":
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
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(user.atk), str(user.money), str(_needAtk), str(_needHp))
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💢 Атака улучшена")                
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="bigkach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="bigkach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
            f = open('1.txt', 'a')
            f.write("\n{}".format(call.from_user.id))
            f.close()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не хватает золота")                
    elif kach == 'hp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.location == "Хэвенбург":
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
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(user.atk), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="bigkach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="bigkach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="❤️Здоровье улучшено")                
            f = open('1.txt', 'a')
            f.write("\n{}".format(call.from_user.id))
            f.close()
            gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не хватает золота")                



@bot.message_handler(commands=['watch_around'])
def watcharound(m):
    if m.from_user.id == m.chat.id:
        pass
    else:
        return
    user = db.Users.get(user_id=m.from_user.id)
    if user.location != 'Город' and user.location != 'Хэвенбург' and user.location != 'Пустыня' and user.location != 'Свалка':
        pass
    else:
        bot.reply_to(m, "В этой локации можно использовать только стандартную навигацию")
        return
    if user.location == 'Первый этаж башни' or user.location == 'Лесная гробница' or user.location == 'Второй этаж башни' or user.location == 'Третий этаж башни' or user.location == 'Четвёртый этаж башни':
        bot.send_message(m.chat.id, "/watch_around недоступен")
        return
    nowProgLoc = user.progLoc
    _pl = nowProgLoc.split('|')
    num = _pl[1]
    users = db.Users.select().where(db.Users.progLoc==user.progLoc, db.Users.id!=user.id, db.Users.location==user.location)
    text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭{}: К-{}\n\nСписок игроков рядом:\n".format(user.nowhp, user.hp, user.energy, user.eat, user.location, num)
    minstats = int((user.atk + user.hp) * 0.7)
    maxstats = int((user.atk + user.hp) * 1.3)
    count = 0
    for z in users:
        if z.atk + z.hp >= minstats and z.atk + z.hp <= maxstats:
            if z.frak == 'Грязное небо': frak = '🌋'
            elif z.frak == 'Вавилон': frak = '🗼'
            elif z.frak == 'Хранители': frak = '💠'
            elif z.frak == 'Небесные рыцари': frak = '⚔️'
            else: frak = "👤"
            text += "\n[{}]{} - /attack_{}".format(frak, z.username, z.id)
            count += 1
    if count == 0:
        text += "К сожалению, рядом никого нет"
    bot.send_message(m.chat.id, text)

@bot.message_handler(func=lambda m:m.text and m.text.startswith('/attack_'))
def attack_(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/attack_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = db.Users.get(user_id=m.from_user.id)
    enemy = db.Users.get(id=result)
    minstats = int((player.atk + player.hp) * 0.7)
    maxstats = int((player.atk + player.hp) * 1.3)
    if int(enemy.atk) + int(enemy.hp) >= int(minstats) and int(enemy.atk) + int(enemy.hp) <= int(maxstats):
        pass
    else:
        bot.send_message(m.chat.id, "Вы не можете драться с этим игроком")
        return
    if player.location == enemy.location and player.progLoc == enemy.progLoc:
        bot.send_message(m.chat.id, '_Ты решил нажиться на чужом разбитом хлебале. Тебе понадобится некоторое время..._', parse_mode='markdown')
        try:
            bot.send_message(enemy.user_id, "_Заиграла настораживающая музыка и появилось ощущение, словно кто-то готовится напасть на тебя. Хм, что бы это могло значить..._", parse_mode='markdown')
        except:
            pass
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pvpbigStart(player, enemy))
    else:
        bot.send_message(m.chat.id, "Игрок уже покинул это место либо вы уже прошли мимо")


async def pvpbigStart(player, enemy):
    await asyncio.sleep(30)
    player = db.Users.get(user_id=player.user_id)
    enemy = db.Users.get(user_id=enemy.user_id)
    if player.user_id == enemy.user_id:
        bot.send_message(player.user_id, "Харакири - удел слабых")
        return
    if player.location == enemy.location and player.progLoc == enemy.progLoc:
        pass
    else:
        bot.send_message(player.user_id, "_Жертва скрылась из виду раньше, чем ты успел на него напасть._", parse_mode='markdown')
        return
    player1 = db.Users.get(user_id=player.user_id)
    player2 = db.Users.get(user_id=enemy.user_id)
    FATK = random.randint(0, 100)
    playerArmor = int(player1.armor / 5)
    enemyArmor = int(player2.armor / 5)
    player = {'username': player1.username, 'armor': playerArmor, 'atk': player1.atk, 'hp': player1.nowhp, 'user_id': player1.user_id}
    enemy = {'username': player2.username, 'armor': enemyArmor, 'atk': player2.atk, 'hp': player2.nowhp, 'user_id': player2.user_id}
    bot.send_message(enemy['user_id'], "👤{} VS 👤{}\n\n\n".format(player['username'], enemy['username']))
    bot.send_message(player['user_id'], "👤{} VS 👤{}\n\n\n".format(player['username'], enemy['username']))
    minPlayerAtk = int(player['atk'] * 0.4)
    maxPlayerAtk = int(player['atk'] * 0.75)
    minEnemyAtk = int(enemy['atk'] * 0.4)
    maxEnemyAtk = int(enemy['atk'] * 0.75)
    if FATK >= 50:
        pAtk = random.randint(minPlayerAtk, maxPlayerAtk)
        if pAtk < enemy['armor']:
            eArmor = pAtk - 1
        else:
            eArmor = enemyArmor
        playerAtk = pAtk - eArmor
        step = 1
        enemy['hp'] = enemy['hp'] - playerAtk
        textPlayer = "👤{} нанес удар {}💥 (🛡{})".format(player['username'], pAtk, eArmor)
        textEnemy = "👤{} нанес удар {}💥 (🛡{})".format(player['username'], pAtk, eArmor)
    else:
        eAtk = random.randint(minEnemyAtk, maxEnemyAtk)
        if eAtk < player['armor']:
            pArmor = eAtk - 1        
        else:
            pArmor = playerArmor
        enemyAtk = eAtk - pArmor
        step = 2
        player['hp'] = player['hp'] - enemyAtk
        textEnemy = "👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], eAtk, pArmor)
        textPlayer = "👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], eAtk, pArmor)
    while player['hp'] > 0 and enemy['hp'] > 0:
        step += 1
        pAtk = random.randint(minPlayerAtk, maxPlayerAtk) 
        if pAtk < enemy['armor']:
            eArmor = pAtk - 1
        else:
            eArmor = enemyArmor
        playerAtk = pAtk - eArmor
        eAtk = random.randint(minEnemyAtk, maxEnemyAtk) 
        if eAtk < player['armor']:
            pArmor = pAtk - 1
        else:
            pArmor = playerArmor
        enemyAtk = eAtk - pArmor
        if step/2 == step//2: #Атака enemy
            player['hp'] = player['hp'] - enemyAtk
            if player['hp'] < 0:
                player['hp'] = 0
            textEnemy += "\n👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], str(eAtk), pArmor)
            textPlayer += "\n👤{} нанес удар {}💥 (🛡{})".format(enemy['username'], str(eAtk), pArmor)
        else: #Атака player
            enemy['hp'] = enemy['hp'] - playerAtk
            if enemy['hp'] < 0:
                enemy['hp'] = 0
            textPlayer += "\n👤{} нанес удар {}💥(🛡{})".format(player['username'], str(pAtk), eArmor)
            textEnemy += "\n👤{} нанес удар {}💥(🛡{})".format(player['username'], str(pAtk), eArmor)
    if player['hp'] <= 0:
        mi = int(player1.money * 0.1)
        ma = int(player1.money * 0.25)
        goldAward = random.randint(mi, ma)
        textPlayer += "\n\n_Тебя знатно потрепали, но не до смерти. Местные оттащили твоё тело в город._\n\nПотеряно: {}💰".format(int(goldAward))
        textEnemy += "\n\n_Ты вышел победителем из этой схватки, заодно обшарил карманы проигравшего._\n\nПолучено: {}💰".format(int(goldAward))
        player1.location = "Хэвенбург"
        player1.position = "Номер в отеле"
        player1.nowhp = random.randint(1, 10)
        player1.money -= goldAward
        player2.money += goldAward
        player2.nowhp = enemy['hp']
    else:
        mi = int(player2.money * 0.1)
        ma = int(player2.money * 0.25)
        goldAward = random.randint(mi, ma)
        textEnemy += "\n\n_Тебя знатно потрепали, но не до смерти. Местные оттащили твоё тело в город._\n\nПотеряно: {}💰".format(int(goldAward))
        textPlayer += "\n\n_Ты вышел победителем из этой схватки, заодно обшарил карманы проигравшего._\n\nПолучено: {}💰".format(int(goldAward))
        player2.location = "Хэвенбург"
        player2.position = "Номер в отеле"
        player2.nowhp = random.randint(1, 10)
        player2.money -= goldAward
        player1.money += goldAward
        player1.nowhp = player['hp']
    player1.save()
    player2.save()
    bot.send_message(player['user_id'], textPlayer, parse_mode = 'markdown')
    bot.send_message(enemy['user_id'], textEnemy, parse_mode = 'markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('navgo'))
def navgo(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    user = db.Users.get(user_id=call.from_user.id)
    user.progStatus = 1
    user.save()
    gg = bot.edit_message_text("Вы отправились в исследование дальше.", call.message.chat.id, call.message.message_id)



@bot.callback_query_handler(func=lambda call: call.data.startswith('dunjgo_'))
def dunjgo(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    user = db.Users.get(user_id=call.from_user.id)
    if kach == 'grob':
        if user.location == 'Случайный лес' and user.progLoc == 'Случайный лес|35':
            user.location = 'Лесная гробница'
            user.progLoc = 'Лесная гробница|1'
            user.progStatus = 1
            text = "Вы направились в лесную гробницу"
            user.save()
        else:
            text = "Вы уже прошли развилку"
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

