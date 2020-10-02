import telebot
from Proxy_services import check_all, check_one_port, check_country
from telebot import types

bot = telebot.TeleBot("1206950757:AAFjG_6ofJW9J9A_K6uOeGYq3eeGnEH8qbo")

# Метод, который получает сообщения и обрабатывает их


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет! Я бот для проверки мобилок")

    elif message.text == "/check":
        # кнопки
        keyboard = types.InlineKeyboardMarkup()
        key_all = types.InlineKeyboardButton(text='Check all', callback_data='call_all')
        keyboard.add(key_all)
        key_one = types.InlineKeyboardButton(text="Check one port", callback_data='call_one')
        keyboard.add(key_one)
        key_c = types.InlineKeyboardButton(text="Check country", callback_data='call_country')
        keyboard.add(key_c)
        bot.send_message(message.from_user.id, text='Выбери тип проверки', reply_markup=keyboard)

    elif message.text == '/check_all':
        check_all(message, bot)

    elif message.text == '/check_port':
        sent = bot.send_message(message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_one_port, bot)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, '/check - выбрать тип проверки \n'
                         '/check_all - проверить все порты \n /check_port - проверить один порт')

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "call_all":
        msg = "Запускаю проверку всех мобилок?"
        # Отправляем текст в Телеграм
        sent = bot.send_message(call.message.chat.id, msg)
        bot.register_next_step_handler(sent, check_all, bot)

    elif call.data == 'call_one':
        sent = bot.send_message(call.message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_one_port, bot)

    elif call.data == 'call_country':
        sent = bot.send_message(call.message.chat.id, 'Какую страну чекаем?')
        bot.register_next_step_handler(sent, check_country, bot)


# Постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
