import time
import random
def pvpcheck(player, call):
    location = "Хэвенбург"
    position = "Арена"
    player1 = db.Users.get(user_id=player)
    location = "Хэвенбург"
    position = "Арена"
    minstats = int((player1.atk + player1.hp) * 0.7)
    maxstats = int((player1.atk + player1.hp) * 1.3)
    player2 = db.Users.select().where(db.Users.location==location, db.Users.position==position, db.Users.user_id != player1.user_id, db.Users.atk + db.Users.hp >= minstats, db.Users.atk + db.Users.hp <= maxstats)
    text = "Подойдя к скучающей даме, она взяла тебя за руку и повела во дворы, на ходу доставая из твоего кармана 35💰 и отвечая, что вернёт, если выиграешь. Через несколько кварталов ты оказался на арене.\nВыбери игрока , с которым хочешь драться или просто жди, пока кто-нибудь выберет тебя:"
    if not player2:
        text = "Подойдя к скучающей даме, она взяла тебя за руку и повела во дворы, на ходу доставая из твоего кармана 35💰 и отвечая, что вернёт, если выиграешь. Через несколько кварталов ты оказался на арене.\nК сожалению, драться сейчас не с кем, но мы запишем тебя в очередь. Подожди немного, авось кто придёт..."
        gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    for dict in player2:
        text += "\n{} - /battle_{}".format(dict.username, dict.user_id)
    gg = bot.edit_message_text(text, call.message.chat.id, call.message.message_id)




@bot.message_handler(func=lambda m:m.text and m.text.startswith('/battle_'))
def battleStarts(m):
    enemy = m.text.replace('/battle_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    result = db.Users.get(user_id=enemy)
    minstats = int((result.atk + result.hp) * 0.7)
    maxstats = int((result.atk + result.hp) * 1.3)
    if int(result.atk) + int(result.hp) >= int(minstats) and int(result.atk) + int(result.hp) <= int(maxstats):
    	pass
    else:
    	bot.send_message(m.chat.id, "Вы не можете драться с этим игроком")
    	return
    if result.location == "Хэвенбург" and result.position == "Арена":
        re = db.Users.get(user_id=m.from_user.id)
        if re.location == "Хэвенбург" and re.position == "Арена":
            player = m.from_user.id
            pvpStart(player, enemy)
        else:
            bot.send_message(m.chat.id, "Вы находитесь не на Арене.")
    else:
        bot.send_message(m.chat.id, "Игрок уже покинул Арену.")


def pvpStart(player, enemy):
    location = "Город"
    position = "Арена"
    player1 = db.Users.get(user_id=player)
    player2 = db.Users.get(user_id=enemy)
    FATK = random.randint(0, 100)
    player = {'username': player1.username, 'atk': player1.atk, 'hp': player1.nowhp, 'user_id': player1.user_id}
    enemy = {'username': player2.username, 'atk': player2.atk, 'hp': player2.nowhp, 'user_id': player2.user_id}
    bot.send_message(enemy['user_id'], "👤{} VS 👤{}\n\n\n".format(player['username'], enemy['username']))
    bot.send_message(player['user_id'], "👤{} VS 👤{}\n\n\n".format(player['username'], enemy['username']))
    minPlayerAtk = int(player['atk'] * 0.25)
    maxPlayerAtk = int(player['atk'] * 0.5)
    minEnemyAtk = int(enemy['atk'] * 0.25)
    maxEnemyAtk = int(enemy['atk'] * 0.5)
    if FATK >= 50:
        playerAtk = random.randint(minPlayerAtk, maxPlayerAtk) 
        step = 1
        enemy['hp'] = enemy['hp'] - playerAtk
        textPlayer = "👤{} нанес удар {}💥".format(player['username'], playerAtk)
        textEnemy = "👤{} нанес удар {}💥".format(player['username'], playerAtk)
    else:
        enemyAtk = random.randint(minEnemyAtk, maxEnemyAtk) 
        step = 2
        player['hp'] = player['hp'] - enemyAtk
        textEnemy = "👤{} нанес удар {}💥".format(enemy['username'], enemyAtk)
        textPlayer = "👤{} нанес удар {}💥".format(enemy['username'], enemyAtk)
    while player['hp'] > 0 and enemy['hp'] > 0:
        step += 1
        playerAtk = random.randint(minPlayerAtk, maxPlayerAtk) 
        enemyAtk = random.randint(minEnemyAtk, maxEnemyAtk) 
        if step/2 == step//2: #Атака enemy
            player['hp'] = player['hp'] - enemyAtk
            if player['hp'] < 0:
                player['hp'] = 0
            textEnemy += "\n👤{} нанес удар {}💥".format(enemy['username'], str(enemyAtk))
            textPlayer += "\n👤{} нанес удар {}💥".format(enemy['username'], str(enemyAtk))
        else: #Атака player
            enemy['hp'] = enemy['hp'] - playerAtk
            if enemy['hp'] < 0:
                enemy['hp'] = 0
            textPlayer += "\n👤{} нанес удар {}💥".format(player['username'], str(playerAtk))
            textEnemy += "\n👤{} нанес удар {}💥".format(player['username'], str(playerAtk))
    if player['hp'] <= 0:
        textPlayer += "\n*Поражение*\nБесчувственного, вас скинули в мимо текущую речку, которая ведёт к источникам."
        textEnemy += "\n*Победа! Ты заработал 15💰*"
        position = "Источники"
        posEnemy = "Площадь"
        player1.position = position
        player1.nowhp = 0
        player2.position = posEnemy
        player2.money = player2.money + 50
    else:
        textEnemy += "\n*Поражение*\nБесчувственного, вас скинули в мимо текущую речку, которая ведёт к источникам."
        textPlayer += "\n*Победа! Ты заработал 15💰*"
        position = "Источники"
        posPlayer = "Площадь"
        player2.position = position
        player2.nowhp = 0
        player1.position = posPlayer
        player1.money = player1.money + 50
    player1.save()
    player2.save()
    bot.send_message(player['user_id'], textPlayer, parse_mode = 'markdown')
    bot.send_message(enemy['user_id'], textEnemy, parse_mode = 'markdown')