import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("6137651503:AAFofB-QV9X2WJkPVCSiGB5vOIxCc-wo3Mg")
nameBD="rdInfoForPK.db"

def dbSelect(userID):
    db = sqlite3.connect(nameBD)
    cursor = db.cursor()
    cursor.execute(f'SELECT bdSelector FROM users WHERE userID="{userID}"')
    dataB = cursor.fetchall()
    cursor.close()
    return dataB
def setCounter(item,userID):
    db = sqlite3.connect(nameBD)
    cursor = db.cursor()
    cursor.execute("UPDATE users SET countbatton = ? WHERE userID = ?", (item, userID))
    db.commit()
    cursor.close()
def getCounter(userID):
    db = sqlite3.connect(nameBD)
    cursor = db.cursor()
    cursor.execute(f'SELECT countbatton FROM users WHERE userID="{userID}"')
    dataB = cursor.fetchall()
    cursor.close()
    return dataB[0][0]
def itemCheck(item_to_check,userID):
    db = sqlite3.connect(nameBD)
    cursor = db.cursor()

    # Запрос для проверки наличия элемента

    query = "SELECT * FROM startButons WHERE buton = ?"
    cursor.execute(query, (item_to_check,))
    result = cursor.fetchone()
    if result:
        query = f"SELECT names FROM startButons WHERE buton = ?"
        cursor.execute(query, (item_to_check,))
        item = cursor.fetchone()

        cursor.execute("UPDATE users SET bdSelector = ? WHERE userID = ?", (item[0], userID))
        db.commit()
    cursor.close()

    return result
#Обрабокта запуска бота



@bot.message_handler(commands=['start'])
def start(message):
    #Создание клавиауры запросов
    db = sqlite3.connect(nameBD)
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE userID = ?"
    cursor.execute(query, (message.from_user.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute(f'INSERT INTO users VALUES("{message.from_user.id}","","")')
        db.commit()
    cursor.execute(f'SELECT * FROM startButons ')
    button_texts = cursor.fetchall()

    keyboard = types.ReplyKeyboardMarkup(row_width=2,  resize_keyboard=True)
    # Добавление кнопок в клавиатуру
    for button_text in button_texts:
        keyboard.add(types.KeyboardButton(button_text[0]))
    bot.send_message(message.chat.id,"Привет! Я твой помошник и готов ответить на часто задаваемые вопросы. Выбери что тебя интересует в меню",reply_markup=keyboard)
    cursor.close()


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):


    db = sqlite3.connect(nameBD)
    cursor = db.cursor()
    counter = dbSelect(call.from_user.id)

    if call.data == "enter":
        setCounter(getCounter(call.from_user.id) + 5, call.from_user.id)
        cursor.execute(f'SELECT questions, rowid FROM {counter[0][0]} ')
        buttons = cursor.fetchall()
        count =  getCounter(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()

        for button in buttons[count:count+5]:
            key = types.InlineKeyboardButton(text=f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)

        if len(buttons)-5 > getCounter(call.from_user.id) :
            row = types.InlineKeyboardButton(text=f'<<Назад', callback_data=f'back'),types.InlineKeyboardButton(text=f'Далее>>', callback_data='enter')
            keyboard.add(*row)
        else:
            keyboard.add(types.InlineKeyboardButton(text=f'<<Назад', callback_data=f'back'))

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    elif call.data == "back":
        cursor.execute(f'SELECT questions, rowid FROM {counter[0][0]} ')
        buttons = cursor.fetchall()
        setCounter(getCounter(call.from_user.id) - 5, call.from_user.id)
        count = getCounter(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()


        for button in buttons[count:count+5]:
            key = types.InlineKeyboardButton(text=f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)

        if  getCounter(call.from_user.id) >= 5:
            row = types.InlineKeyboardButton(text=f'<<Назад', callback_data=f'back'), types.InlineKeyboardButton(
                text=f'Далее>>', callback_data='enter')
            keyboard.add(*row)
        else:
            keyboard.add(types.InlineKeyboardButton(text=f'Далее>>', callback_data=f'enter'))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
    else:
        cursor.execute(f'SELECT * FROM {counter[0][0]} WHERE rowid="{call.data}"')
        list1 = cursor.fetchall()
        print(list1[0][2])
        if list1[0][2] == b'1':
            bot.delete_message(call.message.chat.id,call.message.message_id)
            bot.send_photo(call.message.chat.id, open(list1[0][3], 'rb'), caption=f'{list1[0][1]}')
            print(1)
        else:
            bot.send_message(call.message.chat.id, f"{list1[0][1]}")

        cursor.close()



@bot.message_handler()
def main(message):

    if itemCheck(message.text,message.from_user.id):
        db = sqlite3.connect(nameBD)
        cursor = db.cursor()
        counter = dbSelect(message.from_user.id)
        cursor.execute(f'SELECT questions, rowid FROM {counter[0][0]} ')
        buttons = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        for button in buttons[:5]:
            key = types.InlineKeyboardButton(text = f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)

        if len(buttons) > 5:
            key = types.InlineKeyboardButton(text=f'Далее>>', callback_data='enter')
            keyboard.add(key)
            setCounter(0, message.from_user.id)
        bot.send_message(message.chat.id, text='Выберите кнопку:', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text='Неверная команда')



bot.polling(none_stop=True)