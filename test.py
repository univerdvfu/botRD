import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("")
db = sqlite3.connect('rdInfo.db')
c = db.cursor()
counter = 5

#Обрабокта запуска бота
@bot.message_handler(commands=['start'])
def start(message):
    # Создание пустого списка кнопок
    keyboard = types.InlineKeyboardMarkup()

    # Генерация кнопок с использованием цикла или генератора списков

        # Создание кнопки с уникальным текстом и колбэк-данными
    button1 = types.InlineKeyboardButton(text='Часто задаваемые вопросы про поступление', callback_data='1')
    button2 = types.InlineKeyboardButton(text='Часто задаваемые вопросы про обучение', callback_data='2')
    button3 = types.InlineKeyboardButton(text='Информация о напрвлениях обучение', callback_data='3')
        # Добавление кнопки в список
    keyboard.add(button1, button2, button3)

    # Отправка клавиатуры с кнопками в чат
    bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
    c.close()



@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    # Проверка, была ли нажата кнопка
    if call.data:

        # Кнопка была нажата
        button_data = call.data
        message_id = call.message.message_id
        chat_id = call.message.chat.id

        bot.delete_message(chat_id, message_id)
        db = sqlite3.connect('rdInfo.db')
        c = db.cursor()

        # Выполнение действий в зависимости от нажатой кнопки
        if button_data == 'back':
            bot.delete_message(chat_id, message_id)
            c.execute('SELECT rowid, name_ID FROM info')
            list1 = c.fetchall()

            # Создание пустого списка кнопок
            keyboard = types.InlineKeyboardMarkup()

            # Количество кнопок, которое вы хотите создать

            num_buttons = len(list1)-5

            # Генерация кнопок с использованием цикла или генератора списков
            for i in range(num_buttons):
                # Создание кнопки с уникальным текстом и колбэк-данными
                button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')

                # Добавление кнопки в список
                keyboard.add(button)

            # Отправка клавиатуры с кнопками в чат
            bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)



        elif button_data == 'enter':
            bot.delete_message(chat_id, message_id)
            print(message_id, chat_id)
        else:

            c.execute(f'SELECT text_info FROM info WHERE rowid="{button_data}"')
            list1 = c.fetchall()

            bot.send_message(call.message.chat.id, f"{list1[0][0]}")

        c.close()

#Обработка команд клавиатуры
@bot.message_handler()
def main(message):
    #Обработка Кнопки с вызываом сайта
    if  message.text == 'Информация о напрвлениях обучение':
        markupOnChat = types.InlineKeyboardMarkup()
        btn4 = types.InlineKeyboardButton('russky.digital', url='https://russky.digital/')
        markupOnChat.row(btn4)
        bot.send_message(message.chat.id, "Информация о напрвлениях обучение", reply_markup=markupOnChat)

    # Обработка Кнопки с вызывом вопросов
    elif message.text == 'Часто задаваемые вопросы про обучение':
        db = sqlite3.connect('rdInfo.db')
        c = db.cursor()
        c.execute('SELECT rowid, name_ID FROM info')
        list1 = c.fetchall()

        # Создание пустого списка кнопок
        keyboard = types.InlineKeyboardMarkup()

        # Количество кнопок, которое вы хотите создать
        if  len(list1)>5:
            num_buttons = 5
        else:
            num_buttons = len(list1)

        # Генерация кнопок с использованием цикла или генератора списков
        for i in range(num_buttons):
            # Создание кнопки с уникальным текстом и колбэк-данными
            button = types.InlineKeyboardButton(text=f'{list1[i][1]}', callback_data=f'{list1[i][0]}')

            # Добавление кнопки в список
            keyboard.add(button)

        # Отправка клавиатуры с кнопками в чат
        bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
        c.close()

    # Обработка Кнопки с вызывом вопросов
    elif message.text == 'Часто задаваемые вопросы про поступление':


        # Создание пустого списка кнопок
        keyboard = types.InlineKeyboardMarkup()

        # Количество кнопок, которое вы хотите создать
        num_buttons = 5

        # Генерация кнопок с использованием цикла или генератора списков
        for i in range(num_buttons):
            # Создание кнопки с уникальным текстом и колбэк-данными
            button = types.InlineKeyboardButton(text=f'Button {i + 1}', callback_data=f'button_{i + 1}')

            # Добавление кнопки в список
            keyboard.add(button)

        # Отправка клавиатуры с кнопками в чат
        bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Неверная команда",)


# photo_path = 'IMG_7755-3.jpg'
#
# bot.send_photo(message.chat.id, open(photo_path, 'rb'), caption='Привет! Я отправляю картинку и сообщение.')



bot.polling(none_stop=True)
