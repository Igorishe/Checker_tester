import telebot
from Proxy_services import (
    check_all, check_one_port, check_country, check_rotation,
    timer_check, timer_check_off
)
from telebot import types
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
tg = config['telegram']
token = tg['token']

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.from_user.id,
        'Привет! Я бот для проверки мобилок. Напиши /help'
    )


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.from_user.id,
        '/check - выбрать тип проверки, /'
        ' /monitoring - проверка по таймеру',
    )


@bot.message_handler(commands=['check'])
def check(message):
    markup = types.InlineKeyboardMarkup()
    check_all_ports_button = types.InlineKeyboardButton(
        'All',
        callback_data='call_all',
    )
    check_one_port_button = types.InlineKeyboardButton(
        'One port',
        callback_data='call_one',
    )
    check_country_button = types.InlineKeyboardButton(
        'Country',
        callback_data='call_country',
    )
    check_rotation_button = types.InlineKeyboardButton(
        'Rotation',
        callback_data='call_rotation',
    )
    markup.row(
        check_all_ports_button, check_one_port_button,
        check_country_button, check_rotation_button,
    )
    bot.send_message(
        message.from_user.id,
        text='Выбери тип проверки',
        reply_markup=markup,
    )


@bot.message_handler(commands=['monitoring'])
def monitoring(message):
    markup = types.InlineKeyboardMarkup()
    on_button = types.InlineKeyboardButton(
        'On',
        callback_data='call_monitor_on',
    )
    off_button = types.InlineKeyboardButton(
        'Off',
        callback_data='call_monitor_off',
    )
    markup.row(on_button, off_button)
    bot.send_message(
        message.from_user.id,
        text='Выбери действие',
        reply_markup=markup,
    )


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(
        message.from_user.id,
        "Я тебя не понимаю. Напиши /help"
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
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

    elif call.data == 'call_monitor_on':
        sent = bot.send_message(
            call.message.chat.id,
            'Выберите интервал проверки в часах'
        )
        bot.register_next_step_handler(sent, timer_check, bot)

    elif call.data == 'call_monitor_off':
        sent = bot.send_message(call.message.chat.id, 'Отключаем?')
        bot.register_next_step_handler(sent, timer_check_off, bot)


bot.polling(none_stop=True, interval=0)
