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
    proxy_list = parse_data(get_proxies_by_api())
    msg = ''
    for i in range(len(proxy_list)):
        port = proxy_list[i][2]
        msg_one = check_req(port, proxy_list[i][0])
        msg += msg_one
    bot.send_message(message.chat.id, msg)



def check_req(port, name='1'):
    if name == '1':
        try:
            r = requests.get('http://2ip.ru/', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                         'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
            return f'\u2705 Порт {port} код {str(r.status_code)} Удачно \n'
        except requests.exceptions.ProxyError:
            return f'\u274c Порт {port} Неудачно \n'
    else:
        try:
            r = requests.get('http://2ip.ru/', proxies={'http': f'http://batch:8sdf91sx@37.1.221.45:{port}',
                                                         'https': f'https://batch:8sdf91sx@37.1.221.45:{port}'})
            return f'\u2705 {name} код {str(r.status_code)} Удачно \n'
        except requests.exceptions.ProxyError:
            return f'\u274c {name} Неудачно \n'
