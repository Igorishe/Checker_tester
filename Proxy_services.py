import json
import os
import time

import requests
from dotenv import load_dotenv

from API_functions import get_proxies_by_api, parse_data

load_dotenv()

proxy_login = os.getenv('PROXY_LOGIN')
proxy_pass = os.getenv('PROXY_PASSWORD')
proxy_ip = os.getenv('PROXY_HOST')
proxy_url = os.getenv('CHECK_URL')
ipinfo_token = os.getenv('IPINFO_TOKEN')


def show_in_bot(func):
    """Декоратор для вывода результата работы функции в бот"""
    def wrapper(message, bot):
        text = str(message.text)
        msg = func(text)
        bot.send_message(message.chat.id, msg)
    return wrapper


@show_in_bot
def check_one_port(port):
    """Проверка одного порта"""
    return check_req(port)


@show_in_bot
def check_all(text):
    """Проверка всех мобильных прокси на аккаунте"""
    if text == '+':
        proxy_list = parse_data(get_proxies_by_api())
        msg = ''
        valid = 0
        for i in range(len(proxy_list)):
            port = proxy_list[i][2]
            name = proxy_list[i][0]
            msg_one = check_req(port, name)
            if '\u2705' in msg_one:
                valid += 1
            msg += msg_one
        msg += f'Валидных прокси: {valid} из {len(proxy_list)}'
        return msg
    return 'Check canceled'


@show_in_bot
def check_country(text):
    """Проверка прокси определенной страны"""
    proxy_list = parse_data(get_proxies_by_api())
    msg = ''
    for i in range(len(proxy_list)):
        name = proxy_list[i][0]
        country = name.split(',')[0]
        if country == str(text):
            port = proxy_list[i][2]
            msg_one = check_req(port, name)
            msg += msg_one
    if msg == '':
        return 'Wrong country'
    return msg


def check_req(port, name=None):
    """Тестовый запрос через прокси и анализ ответа"""
    try:
        r = requests.get(
            proxy_url,
            proxies={
                'http': ('http://'
                         f'{proxy_login}:{proxy_pass}@{proxy_ip}:{port}'),
                'https': ('https://'
                          f'{proxy_login}:{proxy_pass}@{proxy_ip}:{port}')
            },
            timeout=(5, 30),
        )
        if r.status_code == 200 and name is None:
            return f'\u2705 Порт {port}\n'
        elif r.status_code == 200 and name is not None:
            return f'\u2705 {name}\n'
        elif r.status_code != 200 and name is None:
            return f'\u274c Порт {port}\n'
        elif r.status_code != 200 and name is not None:
            return f'\u274c {name}\n'
        return 'Something went wrong'
    except (requests.exceptions.ProxyError, requests.exceptions.ReadTimeout):
        if name is None:
            return f'\u2753 Порт {port}\n'
        return f'\u2753 {name}\n'


def check_ipinfo(port):
    """Получает IP-адрес с ipinfo.io"""
    try:
        r = requests.get(
            f'https://ipinfo.io/json?token={ipinfo_token}',
            proxies={
                'http': ('http://'
                         f'{proxy_login}:{proxy_pass}@{proxy_ip}:{port}'),
                'https': ('https://'
                          f'{proxy_login}:{proxy_pass}@{proxy_ip}:{port}')
            }
        )
        resp = json.loads(r.text)
        return resp['ip']
    except requests.exceptions.ProxyError:
        return 'Bad'


@show_in_bot
def check_rotation(port):
    """Проверка наличия ротации IP-адреса"""
    ip1 = check_ipinfo(port)
    time.sleep(300)
    ip2 = check_ipinfo(port)

    if ip1 == 'Bad' or ip2 == 'Bad':
        return '\u274c Bad Requests'
    if ip1 != ip2:
        return '\u2705 Rotation works'
    else:
        return '\u274c No rotation'
