import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("6137651503:AAFofB-QV9X2WJkPVCSiGB5vOIxCc-wo3Mg")
nameBD="rdInfoForPK.db"

count=0
flag= [0,0]

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
        cursor.execute(f'SELECT questions, rowid FROM {counter[0][0]} ')
        buttons = cursor.fetchall()
        count = len(buttons) - getCounter(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        print(buttons[3:1])
        for button in buttons[count:count+5]:
            key = types.InlineKeyboardButton(text=f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)
        if getCounter(call.from_user.id) > 5:
            setCounter(getCounter(call.from_user.id) - 5, call.from_user.id)
            key = types.InlineKeyboardButton(text=f'Далее>>', callback_data='enter')
            keyboard.add(key)
        keyboard.add(types.InlineKeyboardButton(text=f'<<Назад', callback_data=f'back'))
        bot.send_message(call.message.chat.id, text='Выберите кнопку:', reply_markup=keyboard)


    elif call.data == "back":
        cursor.execute(f'SELECT questions, rowid FROM {counter[0][0]} ')
        buttons = cursor.fetchall()
        # setCounter(getCounter(call.from_user.id) + 5, call.from_user.id)
        count = len(buttons) - getCounter(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)


        for button in buttons[count:count+5]:
            key = types.InlineKeyboardButton(text=f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)
        if  getCounter(call.from_user.id) < len(buttons) - 5:
            setCounter(getCounter(call.from_user.id) + 5, call.from_user.id)
            key = types.InlineKeyboardButton(text=f'<<Назад', callback_data='back')
            keyboard.add(key)
        # else:
        #     setCounter(getCounter(call.from_user.id) - 5, call.from_user.id)
        keyboard.add(types.InlineKeyboardButton(text=f'Далее>>', callback_data=f'enter'))
        bot.send_message(call.message.chat.id, text='Выберите кнопку:', reply_markup=keyboard)
    else:


        cursor.execute(f'SELECT * FROM {counter[0][0]} WHERE rowid="{call.data}"')
        list1 = cursor.fetchall()
        if list1[0][2] == "1":
            bot.send_photo(call.message.chat.id, open(list1[0][2], 'rb'), caption=f'{list1[0][0]}')
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

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        for button in buttons[:5]:
            key = types.InlineKeyboardButton(text = f'{button[0]}', callback_data=f'{button[1]}')
            keyboard.add(key)
        if len(buttons) > 5:
            key = types.InlineKeyboardButton(text=f'Далее>>', callback_data='enter')
            keyboard.add(key)
            setCounter(len(buttons) - 5, message.from_user.id)
        bot.send_message(message.chat.id, text='Выберите кнопку:', reply_markup=keyboard)



    else:
        pass

# @bot.callback_query_handler(func=lambda call: True)
# def handle_button_click(call):
#     global selectorDB
#     global count
#     global counter
#     # Проверка, была ли нажата кнопка
#     if call.data:
#         # Кнопка была нажата
#         button_data = call.data
#         message_id = call.message.message_id
#         chat_id = call.message.chat.id
#
#         bot.delete_message(chat_id, message_id)
#         db = sqlite3.connect('rdInfoForPK.db')
#         c = db.cursor()
#         c.execute(f'SELECT rowid, name_ID FROM {selectorDB}')
#         list1 = c.fetchall()
#
#         # if counter % 5 == 0:
#         #     counter-=5
#         if button_data == 'enter':
#             count += 1
#             # Создание пустого списка кнопок
#             keyboard = types.InlineKeyboardMarkup()
#             # Количество кнопок, которое вы хотите создать
#             if (counter // 5 != 0):
#                 num_buttons = 5
#                 counter -= 5
#
#             else:
#                 num_buttons = counter
#             # Генерация кнопок с использованием цикла или генератора списков
#             print(num_buttons, counter)
#             for i in range(num_buttons):
#                 # Создание кнопки с уникальным текстом и колбэк-данными
#                 button = types.InlineKeyboardButton(text=f'{list1[i + (5 * count)][1]}', callback_data=f'{list1[i + (5 * count)][0]}')
#                 # Добавление кнопки в список
#                 keyboard.add(button)
#             if count < ((len(list1) ) // 5):
#                 button = types.InlineKeyboardButton(text=f'Далее', callback_data=f'enter')
#                 keyboard.add(button)
#
#             if count > 0:
#                 button = types.InlineKeyboardButton(text=f'Назад', callback_data=f'back')
#                 keyboard.add(button)
#
#             # Отправка клавиатуры с кнопками в чат
#             bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
#             # Выполнение действий в зависимости от нажатой кнопки
#         elif button_data == 'back':
#             count -= 1
#             counter += 5
#             # Создание пустого списка кнопок
#             keyboard = types.InlineKeyboardMarkup()
#             # Количество кнопок, которое вы хотите создать
#             if counter // 5 != 0:
#                 num_buttons = 5
#
#             else:
#                 num_buttons = counter
#             # Генерация кнопок с использованием цикла или генератора списков
#             print(num_buttons, counter)
#             for i in range(num_buttons):
#                 # Создание кнопки с уникальным текстом и колбэк-данными
#                 button = types.InlineKeyboardButton(text=f'{list1[i + (5 * count)][1]}',
#                                                     callback_data=f'{list1[i + (5 * count)][0]}')
#                 # Добавление кнопки в список
#                 keyboard.add(button)
#             if count < (len(list1) // 5):
#                 button = types.InlineKeyboardButton(text=f'Далее', callback_data=f'enter')
#                 keyboard.add(button)
#             if count > 0:
#                 button = types.InlineKeyboardButton(text=f'Назад', callback_data=f'back')
#                 keyboard.add(button)
#
#             # Отправка клавиатуры с кнопками в чат
#             bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
#
#
#         else:
#
#             c.execute(f'SELECT text_info,flag,URL_img FROM {selectorDB} WHERE rowid="{button_data}"')
#             list1 = c.fetchall()
#             if list1[0][1] == "1":
#                 bot.send_photo(call.message.chat.id, open(list1[0][2], 'rb'), caption=f'{list1[0][0]}')
#             else:
#                 bot.send_message(call.message.chat.id, f"{list1[0][0]}")
#
#         c.close()
#
# #Обработка команд клавиатуры
# @bot.message_handler()
# def main(message):
#     global selectorDB
#     global count
#     global counter
#     global flag
#     #Обработка Кнопки с вызываом сайта
#     if  message.text == 'Информация о напрвлениях обучение':
#         markupOnChat = types.InlineKeyboardMarkup()
#         btn4 = types.InlineKeyboardButton('russky.digital', url='https://russky.digital/')
#         markupOnChat.row(btn4)
#         # bot.send_message(message.chat.id, "Информация о напрвлениях обучение", reply_markup=markupOnChat)
#         bot.send_photo(message.chat.id, open('img/avatar_orange.png', 'rb'), caption='Тут пожробное описание', reply_markup=markupOnChat)
#
#
#
#     # Обработка Кнопки с вызывом вопросов
#     elif message.text == 'Часто задаваемые вопросы про обучение и кампус':
#
#         selectorDB = 'infoCampus'
#         flag= [0,0]
#         count = 0
#         db = sqlite3.connect('rdInfoForPK.db')
#         c = db.cursor()
#         c.execute('SELECT rowid, name_ID FROM infoCampus')
#         list1 = c.fetchall()
#         counter = len(list1) - 5
#
#         # Создание пустого списка кнопок
#         keyboard = types.InlineKeyboardMarkup()
#
#         # Количество кнопок, которое вы хотите создать
#         if  len(list1)>5:
#             num_buttons = 5
#             flag = [1,1]
#         else:
#             num_buttons = len(list1)
#             flag = [0,0]
#
#         # Генерация кнопок с использованием цикла или генератора списков
#         for i in range(num_buttons):
#             # Создание кнопки с уникальным текстом и колбэк-данными
#             button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')
#
#             # Добавление кнопки в список
#             keyboard.add(button)
#         if flag[1]:
#             print(1)
#             button = types.InlineKeyboardButton(text='Далее', callback_data='enter')
#             keyboard.add(button)
#         # Отправка клавиатуры с кнопками в чат
#         bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
#         c.close()
#
#     # Обработка Кнопки с вызывом вопросов
#     elif message.text == 'Часто задаваемые вопросы про поступление':
#         selectorDB = 'info'
#         flag = [0, 0]
#         count = 0
#         db = sqlite3.connect('rdInfoForPK.db')
#         c = db.cursor()
#         c.execute('SELECT rowid, name_ID FROM info')
#         list1 = c.fetchall()
#
#         # Создание пустого списка кнопок
#         keyboard = types.InlineKeyboardMarkup()
#
#         # Количество кнопок, которое вы хотите создать
#         if len(list1) > 5:
#             num_buttons = 5
#             flag = [1, 1]
#         else:
#             num_buttons = len(list1)
#             flag = [0, 0]
#
#         # Генерация кнопок с использованием цикла или генератора списков
#         for i in range(num_buttons):
#             # Создание кнопки с уникальным текстом и колбэк-данными
#             button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')
#
#             # Добавление кнопки в список
#             keyboard.add(button)
#         if flag[1]:
#             print(1)
#             button = types.InlineKeyboardButton(text='Далее', callback_data='enter')
#             keyboard.add(button)
#         # Отправка клавиатуры с кнопками в чат
#         bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
#         c.close()
#
#     else:
#         bot.send_message(message.chat.id, "Неверная команда",)
#
#
# # photo_path = 'IMG_7755-3.jpg'
# #
# # bot.send_photo(message.chat.id, open(photo_path, 'rb'), caption='Привет! Я отправляю картинку и сообщение.')



bot.polling(none_stop=True)
