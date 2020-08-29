import pymysql
import telebot
def on_db():
    db = pymysql.connect(host='localhost',
                         user='rabbit',
                         password='password',                             
                         db='megu',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    return db
devChat = -1001364436303
token = '1025890805:AAHKuwOfB0rGRmK_XdSHrnNhIfjfZ0LgDEE'
bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       

def fixmob():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM monsters WHERE battleStatus = 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        a = 0
        for z in result:
            print("{}".format(z['id']))
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (z['id']))
            res = cursor.fetchone()
            if res and res['battleStatus'] == 1 and res['battleWith'] == z['id']:
                pass
            else:
                sql = "UPDATE monsters SET battleStatus = 0 WHERE id = %s"
                cursor.execute(sql, (z['id']))
                db.commit()
                sql = "UPDATE monsters SET nowhp = hp WHERE id = %s"
                cursor.execute(sql, (z['id']))
                db.commit()
                print("+1 fixed")
                a += 1
        if a >= 5:
            bot.send_message(devChat, "Fixed {} mobs".format(a))
fixmob()