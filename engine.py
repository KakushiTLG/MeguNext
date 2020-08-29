import peewee
import random

database = peewee.MySQLDatabase('megu', user='rabbit', password='password', host='localhost', port=3306)

def ABC(length):
    output = ""
    for x in range(length):
        output += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')
    return output


class Base(peewee.Model):

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return super(Base, cls).get(*args, **kwargs)
        except Exception as e:
            return False

    class Meta:
        database = database


class Battle(Base):
    id = peewee.AutoField(null=False)
    idbattle = peewee.CharField()
    player = peewee.CharField()
    mob = peewee.CharField()

    class Meta:
        db_table = 'battle'


class Donate(Base):
    id = peewee.AutoField(null=False)
    user = peewee.IntegerField()
    summ = peewee.IntegerField()
    status = peewee.IntegerField()
    comment = peewee.CharField()

    class Meta:
        db_table = 'donate'


class Inventory(Base):
    id = peewee.AutoField(null=False)
    idplayer = peewee.IntegerField()
    name = peewee.CharField()
    descr = peewee.CharField()
    type = peewee.CharField()
    bonus = peewee.IntegerField(default=0)
    active = peewee.IntegerField()
    size = peewee.IntegerField()
    
    class Meta:
        db_table = 'inventory'


class Locations(Base):
    id = peewee.AutoField(null=False)
    name = peewee.CharField()
    prev = peewee.CharField()
    next = peewee.CharField()
    size = peewee.IntegerField()
    maxgold = peewee.IntegerField()
    maxexp = peewee.IntegerField()

    class Meta:
        db_table = 'locations'

class Monsters(Base):
    id = peewee.AutoField(null=False)
    name = peewee.CharField()
    atk = peewee.IntegerField()
    hp = peewee.IntegerField()
    nowhp = peewee.IntegerField()
    battleStatus = peewee.IntegerField(default=0)
    battleWith = peewee.IntegerField(null=True)
    location = peewee.CharField()
    pos = peewee.IntegerField()
    maxexp = peewee.IntegerField()
    maxgold = peewee.IntegerField()

    class Meta:
        db_table = 'monsters'

class Shop(Base):
    id = peewee.AutoField(null=False)
    name = peewee.CharField()
    type = peewee.CharField()
    count = peewee.IntegerField()
    price = peewee.IntegerField()

    class Meta:
        db_table = 'shop'

class System(Base):
    id = peewee.AutoField(null=False)
    name = peewee.CharField()
    value = peewee.IntegerField()
    class Meta:
        db_table = 'system'
class Temp(Base):
    id = peewee.AutoField(null=False)
    user_id = peewee.IntegerField()
    count = peewee.IntegerField()
    class Meta:
        db_table = 'temp'

class Fraks(Base):
    name = peewee.CharField(null=False)
    lvl = peewee.IntegerField(null=False)
    exp = peewee.IntegerField(null=False)
    fatk = peewee.IntegerField(null=False)
    atk = peewee.IntegerField(null=False)
    hp = peewee.IntegerField(null=False)
    players = peewee.IntegerField(null=False)
    leader = peewee.IntegerField(null=False)
    fond = peewee.IntegerField(null=False)
    ametist = peewee.IntegerField(null=False)
    rubin = peewee.IntegerField(null=False)
    sapphire = peewee.IntegerField(null=False)
    izumrud = peewee.IntegerField(null=False)
    class Meta:
        db_table = 'fraks'

class Trades(Base):
    id = peewee.AutoField(null=False)
    fromP = peewee.IntegerField()
    toP = peewee.IntegerField()
    item = peewee.IntegerField()
    star = peewee.IntegerField(default=0)
    star2 = peewee.IntegerField(default=0)
    itemreturn = peewee.IntegerField(null=True)
    status = peewee.IntegerField(default=0)
    class Meta:
        db_table = 'trades'

class Users(Base):
    id = peewee.AutoField(null=False)
    username = peewee.CharField()
    user_id = peewee.IntegerField()
    lvl = peewee.IntegerField(default=1)
    exp = peewee.IntegerField(default=0)
    energy = peewee.IntegerField(default=100)
    eat = peewee.IntegerField(default=100)
    money = peewee.IntegerField(default=20)
    almaz = peewee.IntegerField(default=0)
    donatesum = peewee.IntegerField(default=0)
    ref = peewee.CharField(null=True)
    frak = peewee.CharField(null=True)
    location = peewee.CharField(default="Город")
    progLoc = peewee.CharField(default="Город|0")
    progStatus = peewee.IntegerField(default=0)
    position = peewee.CharField(default="Ворота")
    inventorySizeMax = peewee.IntegerField(default=10)
    item = peewee.CharField(null=True)
    atk = peewee.IntegerField(default=5)
    hp = peewee.IntegerField(default=10)
    nowhp = peewee.IntegerField(default=10)
    armor = peewee.IntegerField(default=0)
    battleStatus = peewee.IntegerField(default=0)
    battleWith = peewee.IntegerField(null=True)
    sleepPlayer = peewee.IntegerField(default=0)
    tradecount = peewee.IntegerField(default=0)
    tradenum = peewee.IntegerField(default=3)
    quest = peewee.CharField(null=True)
    questId = peewee.IntegerField(default=0)
    questStatus = peewee.IntegerField(default=0)
    partner = peewee.IntegerField(default=0)
    donatesumPartn = peewee.IntegerField(default=0)
    ban = peewee.IntegerField(default=0)
    banreason = peewee.CharField(null=True)

    class Meta:
        db_table = 'users'


def getInventorySize(user):
    inventory = Inventory.select().where(Inventory.idplayer == user.id, Inventory.active == 1)
    inventorySize = 0
    for dict in inventory:
        name = dict.name
        name, size, bonus = items(name, check=True)
        inventorySize += int(size)
    return inventorySize


def addItem(name, user):
    check = False
    Type, size, bonus = items(name, check=False)
    inventorySize = getInventorySize(user)
    if inventorySize + size > user.inventorySizeMax:
        success = False
    else:
        item = Inventory(name=name, type=Type, size=size, bonus=bonus, active=1, idplayer=user.id)
        item.save()
        success = True
    return success





def items(name, check):
    if name == 'Туннельный свиток':
        name = '📜Туннельный свиток'
        Type = 'Хлам'
        size = 1
        bonus = 0
    if name == 'Донат инв':
        name = 'Донат инв'
        Type = 'Донат'
        size = 0
        bonus = 0
    elif name == 'Бумажный бургер' or name == ' Бумажный бургер':
        name = '🍔Бумажный бургер'
        Type = 'Еда'
        size = 1
        bonus = 13
    elif name == 'Он называет это "яблоко"' or name == ' Он называет это "яблоко"':
        name = '🔴Он называет это "яблоко"'
        Type = 'Еда'
        size = 1
        bonus = 27
    elif name == 'Хер огра' or name == ' Хер огра':
        name = '🥒Хер огра'
        Type = 'Еда'
        size = 1
        bonus = 34
    elif name == 'Бывший сосед' or name == ' Бывший сосед':
        name = '🥩Бывший сосед'
        Type = 'Еда'
        size = 1
        bonus = 38
    elif name == 'Консервы из палеозоя' or name == ' Консервы из палеозоя':
        name = '🥫Консервы из палеозоя'
        Type = 'Еда'
        size = 1
        bonus = 22
    elif name == 'Печенье с предсказанием' or name == ' Печенье с предсказанием':
        name = '🥠Печенье с предсказанием'
        Type = 'Еда'
        size = 1
        bonus = 11
    elif name == 'Лучше не спрашивай' or name == ' Лучше не спрашивай':
        name = '👁‍🗨Лучше не спрашивай'
        Type = 'Еда'
        size = 2
        bonus = 99
    elif name == 'Бывший сосед(поджаренный)' or name == ' Бывший сосед(поджаренный)':
        name = '🥓Бывший сосед(поджаренный)'
        Type = 'Еда'
        size = 1
        bonus = 62
    elif name == 'Большой хер огра':
        name = '🥒Большой хер огра'
        Type = 'Еда'
        bonus = 100
        size = 1
    elif name == 'Кожаный шлем':
        name = '🧢Кожаный шлем'
        Type = 'Броня'
        bonus = 9
        size = 1
    elif name == 'Кожаный нагрудник':
        name = '👕Кожаный нагрудник'
        Type = 'Броня'
        bonus = 15
        size = 2
    elif name == 'Кожаные штаны':
        name = '👖Кожаные штаны'
        Type = 'Броня'
        bonus = 12
        size = 1
    elif name == 'Кожаные ботинки':
        name = '👟Кожаные ботинки'
        Type = 'Броня'
        bonus = 12
        size = 1
    elif name == 'Хоккейная маска':
        name = '🧢Хоккейная маска'
        Type = 'Броня'
        bonus = 21
        size = 1
    elif name == 'Бронежилет':
        name = '👕Бронежилет'
        Type = 'Броня'
        bonus = 39
        size = 2
    elif name == 'Спортивки адидас':
        name = '👖Спортивки адидас'
        Type = 'Броня'
        bonus = 32
        size = 1
    elif name == 'Берцы':
        name = '👟Берцы'
        Type = 'Броня'
        bonus = 21
        size = 1
    elif name == 'Шлем из фольги':
        name = '🧢Шлем из фольги'
        Type = 'Броня'
        bonus = 3
        size = 1
    elif name == 'Майка из пакета':
        name = '👕Майка из пакета'
        Type = 'Броня'
        bonus = 6
        size = 1
    elif name == 'Модные штаны':
        name = '👖Модные штаны'
        Type = 'Броня'
        bonus = 6
        size = 1
    elif name == 'НЕкроссовки':
        name = '👟НЕкроссовки'
        Type = 'Броня'
        bonus = 3
        size = 1
    elif name == 'Шляпа фокусника':
        name = '🎩Шляпа фокусника'
        Type = 'Броня'
        bonus = 20
        size = 1
    elif name == 'Кросы адидас':
        name = '👟Кросы адидас'
        Type = 'Броня'
        bonus = 22
        size = 1
    elif name == 'Комбинезон сталкера':
        name = '👕Комбинезон сталкера'
        Type = 'Броня'
        bonus = 40
        size = 2
    elif name == 'Нижнее бельё Раскуловой':
        name = '👙Нижнее бельё Раскуловой'
        Type = 'Броня'
        bonus = 25
        size = 1
    elif name == 'Тушка питона':
        name = '🐍Тушка питона'
        Type = 'Хлам'
        bonus = 0
        size = 1
    elif name == 'Перо ястреба':
        name = '🦅Перо ястреба'
        Type = 'Хлам'
        bonus = 0
        size = 0
    elif name == 'Свиток телепортации':
        name = '📜Свиток телепортации'
        Type = 'Свиток'
        bonus = 0
        size = 1
    elif name == 'Среднее зелье здоровья':
        name = '🧪Среднее зелье здоровья'
        Type = 'Зелье'
        bonus = 35
        size = 1
    elif name == 'Малое зелье здоровья':
        name = '🧪Малое зелье здоровья'
        Type = 'Зелье'
        bonus = 15
        size = 1
    elif name == 'Большое зелье здоровья':
        name = '🧪Большое зелье здоровья'
        Type = 'Зелье'
        bonus = 55
        size = 1
    elif name == 'Зелье восстановления':
        name = '🧪Зелье восстановления'
        Type = 'Зелье'
        bonus = 0
        size = 2
    elif name == 'Кофе':
        name = '☕️Кофе'
        Type = 'Экипировка'
        bonus = 70
        size = 1
    elif name == 'Улучшенный рюкзак':
        name = '🎒Улучшенный рюкзак'
        Type = 'Экипировка'
        bonus = 0
        size = 0
    elif name == 'Кусок паззла':
        name = '🧩Кусок паззла'
        Type = 'Артефакт'
        bonus = 0
        size = 0
    elif name == 'Волшебные кости':
        name = '🎲Волшебные кости'
        Type = 'Артефакт'
        bonus = 0
        size = 0
    elif name == 'Городской свиток телепортации':
        name = '📜Городской свиток телепортации'
        Type = 'Свиток'
        bonus = 0
        size = 0
    elif name == 'Амулет здоровья':
        name = '🧿Амулет здоровья'
        Type = 'Артефакт'
        bonus = 0
        size = 1
    elif name == 'Маленький сундучок':
        name = '🧳Маленький сундучок'
        Type = 'Сундук'
        bonus = 0
        size = 1
    elif name == 'Шкатулка Кефира':
        name = '🧳Шкатулка Кефира'
        Type = 'Сундук'
        bonus = 0
        size = 1
    elif name == 'Огромный сундук':
        name = '🧳Огромный сундук'
        Type = 'Сундук'
        bonus = 0
        size = 2
    elif name == 'Бесплатная путёвка на свалку':
        name = '🎟Бесплатная путёвка на свалку'
        Type = 'Хлам'
        bonus = 0
        size = 1
    elif name == 'Ashot case':
        name = '🧳Ashot case'
        Type = 'Сундук'
        bonus = 0
        size = 1
    elif name == 'Сун-дук':
        name = '🧳Сун-дук'
        Type = 'Сундук'
        bonus = 0
        size = 1
    elif name == 'Осколок энергии':
        name = '🔷Осколок энергии'
        Type = 'Артефакт'
        bonus = 0
        size = 1
    elif name == 'Кольцо живости':
        name = '💍Кольцо живости'
        Type = 'Артефакт'
        bonus = 0
        size = 1
    elif name == 'Кепка адидас':
        name = '🧢Кепка адидас'
        Type = 'Броня'
        bonus = 28
        size = 1    
    elif name == 'Ночнушка Раскуловой':
        name = '👚Ночнушка Раскуловой'
        Type = 'Броня'
        bonus = 43
        size = 2    
    elif name == 'Штаны Ашодас':
        name = '👖Штаны Ашодас'
        Type = 'Броня'
        bonus = 36
        size = 1    
    elif name == 'Туфельки Раскуловой':
        name = '👠Туфельки Раскуловой'
        Type = 'Броня'
        bonus = 24
        size = 1   
    elif name == 'Положительный тест на беременность':
        name = '🌡Положительный тест на беременность'
        Type = 'Хлам'
        bonus = 0
        size = 1  
    elif name == 'Отрицательный тест на беременность':
        name = '🌡Отрицательный тест на беременность'
        Type = 'Хлам'
        bonus = 0
        size = 1  
    elif name == 'Детектор аномалий':
        name = '📟Детектор аномалий'
        Type = 'Хлам'
        bonus = 0
        size = 1  
    elif name == 'Аптечка':
        name = '🧳Аптечка'
        Type = 'Сундук'
        bonus = 0
        size = 1
    elif name == 'Успокаивающее':
        name = '💉Успокаивающее'
        Type = 'Зелье'
        bonus = 35
        size = 0  
    elif name == 'Колпак главврача':
        name = '🧢Колпак главврача'
        Type = 'Броня'
        bonus = 15
        size = 1   
    elif name == 'Халат главрача':
        name = '👕Халат главрача'
        Type = 'Броня'
        bonus = 24
        size = 1   
    elif name == 'Штаны главврача':
        name = '👖Штаны главврача'
        Type = 'Броня'
        bonus = 21
        size = 1   
    elif name == 'Тапочки главврача':
        name = '👟Тапочки главврача'
        Type = 'Броня'
        bonus = 18
        size = 1   
    elif name == 'Амфора экстренной помощи':
        name = '🏺Амфора экстренной помощи'
        Type = 'Сундук'
        bonus = 0
        size = 0   
    if check == True: return name, size, bonus
    else: return Type, size, bonus



def specialItems(name, user):
    if name == '🎒Улучшенный рюкзак':
        user.inventorySizeMax = user.inventorySizeMax + 5
        user.save()
        item = Inventory.get(name='Улучшенный рюкзак', idplayer=user.id)
        item.active = 0
        item.save()
    return



def winnerHeal(location):
    chance = random.randint(1, 100)
    if location == 'Пустыня':
        if chance <= 70:
            item = 'Малое зелье здоровья'
        elif chance > 70 and chance <= 95:
            item = 'Среднее зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Случайный лес':
        if chance <= 50:
            item = 'Малое зелье здоровья'
        elif chance < 50 and chance >= 75:
            item = 'Среднее зелье здоровья'
        elif chance < 75 and chance >= 85:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Свалка':
        if chance <= 50:
            item = 'Малое зелье здоровья'
        elif chance < 50 and chance >= 75:
            item = 'Среднее зелье здоровья'
        elif chance < 75 and chance >= 85:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Большая свалка':
        if chance <= 30:
            item = 'Малое зелье здоровья'
        elif chance < 30 and chance >= 55:
            item = 'Среднее зелье здоровья'
        elif chance < 55 and chance >= 80:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    else:
        pass
    return item



def questItems(idp):
    mob = Monsters.get(id=idp.battleWith, battleStatus=1)
    if idp.questId == 1 and idp.questStatus == 1 and mob and mob.name == '🐍 Змея':
        rand = random.randint(1, 100)
        print('random questItems {}'.format(rand))
        success = addItem('Тушка питона', idp)
        if success == True:
            text = "\nНайдена тушка питона\n"
        else:
            text = "\nНайдена тушка питона, но вам некуда её взять. Вы прошли мимо\n"
    elif idp.questId == 2 and idp.questStatus == 1 and mob and mob.name == '🦅 Ястреб':
        rand = random.randint(1, 100)
        print('random questItems {}'.format(rand))
        if rand <= 70:
            success = addItem('Перо ястреба', idp)
            if success == True:
                text = "\nВыдрано перо ястреба\n"
            else:
                text = "\nВы могли бы выдрать перо ястреба, но вам некуда его взять. Вы прошли мимо\n"
        elif rand > 70 and rand < 75:
            success = addItem('Перо ястреба', idp)
            success = addItem('Перо ястреба', idp)
            success = addItem('Перо ястреба', idp)
            if success == True:
                text = "\nВыдрано 3 пера ястреба\n"
            else:
                text = "\nВы могли бы выдрать перо ястреба, но вам некуда его взять. Вы прошли мимо\n"
        else:
            text = ''
    else:
        text = ''
    return text



def winner(idp, location):
    sometext = ""
    player = Users.get(id=idp.id)
    text = questItems(player)
    sometext += text
    mob = Monsters.get(id=idp.battleWith)
    minexp = int(mob.maxexp * 0.7)
    mingold = int(mob.maxgold * 0.7)
    exp = random.randint(minexp, int(mob.maxexp))
    gold = random.randint(mingold, int(mob.maxgold))
    idp.exp = idp.exp + exp
    needExp = idp.lvl * 100
    randomItem = random.randint(1, 100)
    if location == 'Пустыня':
        if randomItem <= 8:
            _items = ['Бумажный бургер', 'Он называет это "яблоко"', 'Хер огра', 'Бывший сосед', 
                'Консервы из палеозоя', 'Бывший сосед(поджаренный)']
            item = random.choice(_items)
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 8 and randomItem <= 10:
            item = winnerHeal(location)
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 10 and randomItem <= 17:
            item = 'Свиток телепортации'
            success = addItem('Свиток телепортации', idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 17 and randomItem <= 32:
            item = 'Маленький сундучок'
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
    elif idp.location == 'Случайный лес':
        if randomItem <= 5:
            _items = ['Бумажный бургер', 'Он называет это "яблоко"', 'Хер огра', 'Бывший сосед', 
                'Консервы из палеозоя', 'Бывший сосед(поджаренный)']
            item = random.choice(_items)
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 13 and randomItem <= 15:
            item = 'Свиток телепортации'
            success = addItem('Свиток телепортации', idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 15 and randomItem <= 37:
            item = 'Огромный сундук'
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 37 and randomItem <= 43:
            item = 'Кофе'
            success = addItem(item, idp)
            name, size, bonus = items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        if mob.name == '💅Депрессивная школьница':
            rand = random.randint(1, 100)
            if rand <= 25:
                success = addItem('Положительный тест на беременность', idp)
                name, size, bonus = items('Положительный тест на беременность', check=True)
                if success == True:
                    sometext += "\n{}".format(name)
    elif idp.location == 'Пустыня':
        if mob.name == '🔸Шаи-Хулуд🔸':
            tunnelItem = 'Туннельный свиток'
            check = Inventory.get(name=tunnelItem, idplayer=idp.id)
            if check:
                pass
            else:
                success = addItem(tunnelItem, idp)
                name, size, bonus = items(tunnelItem, check=True)
                if success == True:
                    sometext += "\n" + name
                if success and success == False:
                    sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
    elif player.location == '🏥Логово сектантов':
        if mob.name == ' 🚑Главврач':
            success = addItem('Аптечка', idp)
            name, size, bonus = items('Аптечка', check=True)
            if success == True:
                sometext += "\n" + name
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
#                success = addItem('Кусок паззла', idp)
#                text = "\nНайден 🧩Кусок паззла\n"
#            if rand > 25 and rand <= 50:
#                success = addItem('Зелье восстановления', idp)
#                if success == True:
#                    text = "\nНайдено Зелье восстановления\n"
#                else:
#                    text = "\nВы что-то нашли, но вам некуда это взять. Пришлось оставить вещь позади\n"
#                success = addItem('Волшебные кости', idp)
#                text += "\nНайдены 🎲Волшебные кости\n"
#    if idp.location == 'Случайный лес':
#        if mob.name == 'Депрессивный Кефир':
#            rand = random.randint(1, 100)
#            if rand <= 25:
#                success = addItem('Кусок паззла', idp)
#                text = "\nНайден 🧩Кусок паззла\n"
#            if rand > 25 and rand <= 50:
#                success = addItem('Зелье восстановления', idp)
#                if success == True:
#                    text = "\nНайдено Зелье восстановления\n"
#                else:
#                    text = "\nВы что-то нашли, но вам некуда это взять. Пришлось оставить вещь позади\n"
#                success = addItem('Волшебные кости', idp)
#                text += "\nНайдены 🎲Волшебные кости\n"
#            inv = Inventory.get(idplayer=idp.id, name='Городской свиток телепортации')
#            if inv:
#                pass
#            else:
#                success = addItem('Городской свиток телепортации', idp)
#                name, size, bonus = items('Городской свиток телепортации', check=True)
#                sometext += "\n📜Городской свиток телепортации"
    if idp.exp >= needExp:
        idp.lvl += 1
        idp.exp = 0
        idp.nowhp = idp.hp
        idp.eat = 100
        idp.energy = 100
        import telebot
        token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
        bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
        bot.send_message(-1001317123616, "Игрок {} теперь {} уровня!".format(idp.username, idp.lvl))
        sometext += "\n✨Вы получили новый уровень. Здоровье, энергия и сытость восстановлены.✨"
        if idp.lvl == 5 and idp.ref:
            refer = Users.get(user_id=idp.ref)
            refer.money += 200
            refer.save()
            try:
                token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
                bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
                bot.send_message(refer.user_id, "Ваш реферал {} достиг 5 уровня. Вы получили 150💰 + 50 акционных!".format(idp.username))
            except:
                pass
    idp.money = idp.money + gold
    idp.save()

    return gold, exp, sometext



