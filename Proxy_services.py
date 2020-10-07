import requests
from API_functions import get_proxies_by_api, parse_data
import json


def check_one_port(message, bot):
    port = str(message.text)
    msg = check_req(port)
    bot.send_message(message.chat.id, msg)


def get_proxies_txt(file):
    f = open(file, 'r')
    proxy_list = f.readlines()
    f.close()
    for i in range(len(proxy_list)):
        proxy_list[i] = proxy_list[i].replace("\n", "")
    return proxy_list


def check_all(message, bot):
    proxy_list = parse_data(get_proxies_by_api())
    msg = ''
    for i in range(len(proxy_list)):
        if i < len(proxy_list)/2 + 1 and i > len(proxy_list)/2:
            bot.send_message(message.chat.id, 'Уже половину чекнул, осталось немного')
        port = proxy_list[i][2]
        name = proxy_list[i][0]
        msg_one = check_req(port, name)
        msg += msg_one
    bot.send_message(message.chat.id, msg)


def check_country(message, bot):
    proxy_list = parse_data(get_proxies_by_api())
    msg = ''
    for i in range(len(proxy_list)):
        name = proxy_list[i][0]
        country = name.split(',')[0]
        if country == str(message.text):
            port = proxy_list[i][2]
            msg_one = check_req(port, name)
            msg += msg_one
    bot.send_message(message.chat.id, msg)


def check_req(port, name='1'):
    try:
        r = requests.get('http://2ip.ru/', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                    'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
        if r.status_code == 200 and name == '1':
            return f'\u2705 Порт {port} код {str(r.status_code)} Удачно \n'
        elif r.status_code == 200 and len(name) > 1:
            return f'\u2705 {name} код {str(r.status_code)} Удачно \n'
        elif r.status_code != 200 and name == '1':
            return f'\u274c Порт {port} код не 200 \n'
        elif r.status_code != 200 and len(name) > 1:
            return f'\u274c {name} Код не 200 \n'
        else:
            return 'Something went wrong'
    except requests.exceptions.ProxyError:
        if name == '1':
            return f'\u274c Порт {port} Неудачно \n'
        else:
            return f'\u274c {name} Неудачно \n'


def check_req_ipinfo(port):
    try:
        r = requests.get('https://ipinfo.io/json?token=76f257fa5ecb74', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                    'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
        resp = json.loads(r.text)
        return resp['ip']
    except requests.exceptions.ProxyError:
        return 'Bad'



