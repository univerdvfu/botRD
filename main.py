import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("6137651503:AAFofB-QV9X2WJkPVCSiGB5vOIxCc-wo3Mg")
db = sqlite3.connect('rdInfo.db')
c = db.cursor()
counter = 5
count=0
flag= [0,0]
selectorDB=''
#Обрабокта запуска бота
@bot.message_handler(commands=['start'])
def start(message):
    #Создание клавиауры запросов
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Часто задаваемые вопросы про поступление")

    btn2 = types.KeyboardButton("Часто задаваемые вопросы про обучение и кампус")
    markup.row(btn1,btn2)
    btn3 = types.KeyboardButton("Информация о напрвлениях обучение")
    markup.row(btn3)
    bot.send_message(message.chat.id,"Привет! Я твой помошник и готов ответить на часто задаваемые вопросы. Выбери что тебя интересует в меню",reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    global selectorDB
    global count
    global counter
    # Проверка, была ли нажата кнопка
    if call.data:
        # Кнопка была нажата
        button_data = call.data
        message_id = call.message.message_id
        chat_id = call.message.chat.id

        bot.delete_message(chat_id, message_id)
        db = sqlite3.connect('rdInfoForPK.db')
        c = db.cursor()
        c.execute(f'SELECT rowid, name_ID FROM {selectorDB}')
        list1 = c.fetchall()

        # if counter % 5 == 0:
        #     counter-=5
        if button_data == 'enter':
            count += 1
            # Создание пустого списка кнопок
            keyboard = types.InlineKeyboardMarkup()
            # Количество кнопок, которое вы хотите создать
            if (counter // 5 != 0):
                num_buttons = 5
                counter -= 5
            else:
                num_buttons = counter
            # Генерация кнопок с использованием цикла или генератора списков
            print(num_buttons,count,counter)
            for i in range(num_buttons):
                # Создание кнопки с уникальным текстом и колбэк-данными
                button = types.InlineKeyboardButton(text=f'{list1[i + (5 * count)][1]}',
                                                    callback_data=f'{list1[i + (5 * count)][0]}')
                # Добавление кнопки в список
                keyboard.add(button)
            if count < ((len(list1) - 1) // 5):
                button = types.InlineKeyboardButton(text=f'Далее', callback_data=f'enter')
                keyboard.add(button)

            if count > 0:
                button = types.InlineKeyboardButton(text=f'Назад', callback_data=f'back')
                keyboard.add(button)

            # Отправка клавиатуры с кнопками в чат
            bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
            # Выполнение действий в зависимости от нажатой кнопки
        elif button_data == 'back':
            count -= 1
            counter += 5
            # Создание пустого списка кнопок
            keyboard = types.InlineKeyboardMarkup()
            # Количество кнопок, которое вы хотите создать
            if counter // 5 != 0:
                num_buttons = 5
                counter -= 5
            else:
                num_buttons = counter
            # Генерация кнопок с использованием цикла или генератора списков
            print(counter, num_buttons, count)
            for i in range(num_buttons):
                # Создание кнопки с уникальным текстом и колбэк-данными
                button = types.InlineKeyboardButton(text=f'{list1[i + (5 * count)][1]}',
                                                    callback_data=f'{list1[i + (5 * count)][0]}')
                # Добавление кнопки в список
                keyboard.add(button)
            if count < (len(list1) // 5):
                button = types.InlineKeyboardButton(text=f'Далее', callback_data=f'enter')
                keyboard.add(button)
            if count > 0:
                button = types.InlineKeyboardButton(text=f'Назад', callback_data=f'back')
                keyboard.add(button)

            # Отправка клавиатуры с кнопками в чат
            bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)


        else:

            c.execute(f'SELECT text_info,flag,URL_img FROM {selectorDB} WHERE rowid="{button_data}"')
            list1 = c.fetchall()
            if list1[0][1] == "1":
                bot.send_photo(call.message.chat.id, open(list1[0][2], 'rb'), caption=f'{list1[0][0]}')
            else:
                bot.send_message(call.message.chat.id, f"{list1[0][0]}")

        c.close()

#Обработка команд клавиатуры
@bot.message_handler()
def main(message):
    global selectorDB
    global count
    global flag
    global counter

    #Обработка Кнопки с вызываом сайта
    if  message.text == 'Информация о напрвлениях обучение':
        selectorDB = 'infoDirection'
        flag = [0, 0]
        count = 0
        db = sqlite3.connect('rdInfoForPK.db')
        c = db.cursor()
        c.execute('SELECT rowid, name_ID FROM infoDirection')
        list1 = c.fetchall()
        counter = len(list1) - 5
        # Создание пустого списка кнопок
        keyboard = types.InlineKeyboardMarkup()

        # Количество кнопок, которое вы хотите создать
        if len(list1) > 5:
            num_buttons = 5
            flag = [1, 1]
        else:
            num_buttons = len(list1)
            flag = [0, 0]

        # Генерация кнопок с использованием цикла или генератора списков
        for i in range(num_buttons):
            # Создание кнопки с уникальным текстом и колбэк-данными
            button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')

            # Добавление кнопки в список
            keyboard.add(button)
        if flag[1]:
            print(1)
            button = types.InlineKeyboardButton(text='Далее', callback_data='enter')
            keyboard.add(button)
        # Отправка клавиатуры с кнопками в чат
        bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
        c.close()



    # Обработка Кнопки с вызывом вопросов
    elif message.text == 'Часто задаваемые вопросы про обучение и кампус':
        selectorDB = 'infoCampus'
        flag= [0,0]
        count = 0
        db = sqlite3.connect('rdInfoForPK.db')
        c = db.cursor()
        c.execute('SELECT rowid, name_ID FROM infoCampus')
        list1 = c.fetchall()
        counter = len(list1) - 5
        # Создание пустого списка кнопок
        keyboard = types.InlineKeyboardMarkup()

        # Количество кнопок, которое вы хотите создать
        if  len(list1)>5:
            num_buttons = 5
            flag = [1,1]
        else:
            num_buttons = len(list1)
            flag = [0,0]

        # Генерация кнопок с использованием цикла или генератора списков
        for i in range(num_buttons):
            # Создание кнопки с уникальным текстом и колбэк-данными
            button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')

            # Добавление кнопки в список
            keyboard.add(button)
        if flag[1]:
            print(1)
            button = types.InlineKeyboardButton(text='Далее', callback_data='enter')
            keyboard.add(button)
        # Отправка клавиатуры с кнопками в чат
        bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
        c.close()

    # Обработка Кнопки с вызывом вопросов
    elif message.text == 'Часто задаваемые вопросы про поступление':
        selectorDB = 'info'
        flag = [0, 0]
        count = 0
        db = sqlite3.connect('rdInfoForPK.db')
        c = db.cursor()
        c.execute('SELECT rowid, name_ID FROM info')
        list1 = c.fetchall()
        counter = len(list1) - 5
        # Создание пустого списка кнопок
        keyboard = types.InlineKeyboardMarkup()

        # Количество кнопок, которое вы хотите создать
        if len(list1) > 5:
            num_buttons = 5
            flag = [1, 1]
        else:
            num_buttons = len(list1)
            flag = [0, 0]

        # Генерация кнопок с использованием цикла или генератора списков
        for i in range(num_buttons):
            # Создание кнопки с уникальным текстом и колбэк-данными
            button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')

            # Добавление кнопки в список
            keyboard.add(button)
        if flag[1]:
            print(1)
            button = types.InlineKeyboardButton(text='Далее', callback_data='enter')
            keyboard.add(button)
        # Отправка клавиатуры с кнопками в чат
        bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
        c.close()

    else:
        bot.send_message(message.chat.id, "Неверная команда",)


# photo_path = 'IMG_7755-3.jpg'
#
# bot.send_photo(message.chat.id, open(photo_path, 'rb'), caption='Привет! Я отправляю картинку и сообщение.')



bot.polling(none_stop=True)
