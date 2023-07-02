import telebot
from telebot import types
import sqlite3

list1= [ ]
bot = telebot.TeleBot("6137651503:AAFofB-QV9X2WJkPVCSiGB5vOIxCc-wo3Mg")


def check_element_exists(table_name, column_name, value):
    global list1
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('rdInfoForPK.db')
    cursor = conn.cursor()

    # Выполняем запрос SELECT с условием
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (value,))


    # Извлекаем результат
    result = cursor.fetchone()[0]
    cursor.execute(f"SELECT text_info FROM {table_name} WHERE {column_name}")
    list1 = cursor.fetchone()
    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    # Возвращаем True, если элемент существует, и False в противном случае
    return result

def drowBatons(selector,counter):
    conn = sqlite3.connect('rdInfoForPK.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT rowid, name_ID FROM {selector}')
    for i in range(num_buttons):
        # Создание кнопки с уникальным текстом и колбэк-данными
        button = types.InlineKeyboardButton(
            text=f'{list1[i][1]}',
            callback_data=f'{list1[i][0]}')

        # Добавление кнопки в список
        keyboard.add(button)
    if flag[1]:
        print(1)
        button = types.InlineKeyboardButton(
            text='Далее', callback_data='enter')
        keyboard.add(button)
    # Отправка клавиатуры с кнопками в чат
    bot.send_message(message.chat.id,
                     'Выберите кнопку:',
                     reply_markup=keyboard)
    c.close()

@bot.message_handler(commands=['start'])

def start(message):
    global list1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    db = sqlite3.connect('rdInfoForPK.db')
    c = db.cursor()
    c.execute('SELECT rowid, name_ID, text_info FROM butons')
    list1 =c.fetchall()
    # print(len(list1))
    for i in range(0,len(list1),2):

        if  i < len(list1)-1:
            # print(i)
            markup.row(types.KeyboardButton(list1[i][1]), types.KeyboardButton(list1[i+1][1]))
        else:
            markup.row(types.KeyboardButton(list1[i][1]))

    bot.send_message(message.chat.id, 'Выберите опцию:',reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    # Проверка, была ли нажата кнопка
    if call.data:
        # Кнопка была нажата
        button_data = call.data
        message_id = call.message.message_id
        chat_id = call.message.chat.id

        bot.delete_message(chat_id, message_id)
        if button_data == 'enter':
            pass
        elif button_data == 'back':
            pass
        else:
           pass
        c.close()

@bot.message_handler()
def main(message):
    global list1

    if check_element_exists('butons', 'name_ID',message.text):

        drowBatons(list1,0)


    else:
        bot.send_message(message.chat.id, "Неверная команда")




bot.polling(none_stop=True)
