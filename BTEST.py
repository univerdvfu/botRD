import sqlite3

db = sqlite3.connect('rdInfoForPK.db')

c = db.cursor()

# c.execute("""
# CREATE TABLE info(
# name_ID text,
# text_info text,
# flag BLOB,
# URL_img text
# )
# """
# )

# c.execute("""
# CREATE TABLE infoCampus(
# name_ID text,
# text_info text,
# flag BLOB,
# URL_img text
# )
# """
# )
#
# c.execute('INSERT INTO info VALUES("Допольнительне баллы зв достижения","Спортивные достижения, олимпиады и документ об образовании с отличием могут увеличить твой шанс на поступление 🔥 Смотри на пикче, за какие индивидуальные достижения дают дополнительные быллы❗️Максимальное количество — 10 баллов. Суммируй различные достижения [например, значок ГТО и статус призера олимпиады], либо приложи к документам аттестат или диплом о СПО с отличием/удостоверение мастера спорта или мастера спорта международного класса","1","img/photo_2023-04-05_12-31-01.jpg")')
# c.execute('INSERT INTO infoCampus VALUES("Дорогое такси?","Не дороже личного верблюда","0","")')
# # c.execute('UPDATE infoCampus SET URL_img = "img/IMG_7755-3.jpg" WHERE name_ID = "Есть ли кто-то кроме лисов на кампусе"')
# c.execute(' SELECT * FROM infoCampus ')
#
# print(0!=0)
#
# db.commit()
# # db.close()
#
# db = sqlite3.connect("rdInfoForPK.db")
# cursor = db.cursor()
# cursor.execute(f'SELECT * FROM startButons ')
# butons = cursor.fetchone()
# print(butons)
import telebot
import sqlite3

# Создание экземпляра бота
bot = telebot.TeleBot('6137651503:AAFofB-QV9X2WJkPVCSiGB5vOIxCc-wo3Mg')

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы для хранения переменных пользователей
cursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, variable TEXT)")

# Обработчик команды /set_variable
@bot.message_handler(commands=['set_variable'])
def set_variable(message):
    user_id = message.from_user.id
    variable_value = message.text.split()[1]

    # Сохранение значения переменной пользователя в базе данных
    cursor.execute("INSERT OR REPLACE INTO Users (user_id, variable) VALUES (?, ?)", (user_id, variable_value))
    conn.commit()

    bot.reply_to(message, "Значение переменной успешно установлено!")

# Обработчик команды /get_variable
@bot.message_handler(commands=['get_variable'])
def get_variable(message):
    user_id = message.from_user.id

    # Получение значения переменной пользователя из базы данных
    cursor.execute("SELECT variable FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        variable_value = result[0]
        bot.reply_to(message, f"Значение переменной: {variable_value}")
    else:
        bot.reply_to(message, "Переменная не найдена!")

# Запуск бота
bot.polling()

# Закрытие соединения с базой данных
conn.close()