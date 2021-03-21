import configparser
import time

import requests
import telebot
from telebot import types

from Proxy_services import (
    check_all, check_one_port, check_country, check_rotation,
)
from Keyboard_services import country_keyboard


config = configparser.ConfigParser()
config.read('config.ini')
tg = config['telegram']
token = tg['token']
allowed_users = [int(i) for i in config['users']['pack'].split(',')]

bot = telebot.TeleBot(token)


def access_check(message):
    return message.from_user.id in allowed_users


@bot.message_handler(func=access_check, commands=['start', 'help'])
def start(message):
    bot.send_message(
        message.from_user.id,
        'Привет! Я бот для проверки мобилок. /check - выбрать тип проверки'
    )


@bot.message_handler(func=access_check, commands=['check'])
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


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(
        message.from_user.id,
        ("Я тебя не понимаю. "
         "Напиши разработчикам свой telegram id, чтобы авторизоваться")
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "call_all":
        msg = "Запускаю проверку всех мобилок? Отправь + чтобы подтвердить"
        sent = bot.send_message(call.message.chat.id, msg)
        bot.register_next_step_handler(sent, check_all, bot)

    elif call.data == 'call_one':
        sent = bot.send_message(call.message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_one_port, bot)

    elif call.data == 'call_country':
        sent = bot.send_message(
            call.message.chat.id,
            'Какую страну чекаем?',
            reply_markup=country_keyboard()
        )
        bot.register_next_step_handler(sent, check_country, bot)

    elif call.data == 'call_rotation':
        sent = bot.send_message(call.message.chat.id, 'Введите порт')
        bot.register_next_step_handler(sent, check_rotation, bot)


while True:
    try:
        bot.polling(none_stop=True)
    except requests.exceptions.ReadTimeout:
        time.sleep(15)
