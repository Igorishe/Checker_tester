import requests
from API_functions import get_proxies_by_api, parse_data


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
    # proxy_list = get_proxies_txt('1.txt')
    proxy_list = parse_data(get_proxies_by_api())
    for i in range(len(proxy_list)):
        port = proxy_list[i][2]
        msg = check_req(port, proxy_list[i][0])
        bot.send_message(message.chat.id, msg)
    bot.send_message(message.chat.id, 'Finished!')


def check_req(port, name='1'):
    if name == '1':
        try:
            r = requests.get('https://2ip.ru/', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                         'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
            return f'Порт {port} код {str(r.status_code)} Удачно'
        except requests.exceptions.ProxyError:
            return f'Порт {port} Неудачно'
    else:
        try:
            r = requests.get('https://2ip.ru/', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                         'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
            return f'{name} код {str(r.status_code)} Удачно'
        except requests.exceptions.ProxyError:
            return f'{name} Неудачно'
