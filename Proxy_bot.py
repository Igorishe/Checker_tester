import telebot
from Proxy_services import check_all, check_one_port, check_country, check_rotation
from telebot import types
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
tg = config['telegram']
token = tg['token']

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Метод, который получает сообщения и обрабатывает их"""
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет! Я бот для проверки мобилок")

    elif message.text == "/check":
        # кнопки
        keyboard = types.InlineKeyboardMarkup()
        key_all = types.InlineKeyboardButton(text='Check all',
                                             callback_data='call_all')
        keyboard.add(key_all)

        key_one = types.InlineKeyboardButton(text='Check one port',
                                             callback_data='call_one')
        keyboard.add(key_one)

        key_c = types.InlineKeyboardButton(text='Check country',
                                           callback_data='call_country')
        keyboard.add(key_c)

        key_rotation = types.InlineKeyboardButton(text='Check rotation',
                                           callback_data='call_rotation')
        keyboard.add(key_rotation)

        bot.send_message(message.from_user.id,
                         text='Выбери тип проверки', reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, '/check - выбрать тип проверки')

    else:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. Напиши /help")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """Обрабатывает нажатия на кнопки"""
    if call.data == "call_all":
        msg = "Запускаю проверку всех мобилок?"
        sent = bot.send_message(call.message.chat.id, msg)
        bot.register_next_step_handler(sent, check_all, bot)

    elif call.data == 'call_one':
        sent = bot.send_message(call.message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_one_port, bot)

    elif call.data == 'call_country':
        sent = bot.send_message(call.message.chat.id, 'Какую страну чекаем?')
        bot.register_next_step_handler(sent, check_country, bot)

    elif call.data == 'call_rotation':
        sent = bot.send_message(call.message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_rotation, bot)


#Поддержание связи с ботом
bot.polling(none_stop=True, interval=0)
