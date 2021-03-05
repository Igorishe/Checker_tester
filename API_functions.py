from requests import Request, Session
import json
import configparser


config = configparser.ConfigParser()

config.read('config.ini')
auth_id = config['rs']['id']
auth_key = config['rs']['key']


def get_proxies_by_api():
    """Получает все пакеты с РС"""
    s = Session()
    headers = {
        'X-Auth-ID': auth_id,
        'X-Auth-Key': auth_key
    }
    url = 'https://rsocks.net/api/v1/file/get-proxy'
    req = Request('POST', url, data='', headers=headers)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    return resp.text


def parse_data(api_obj):
    """Выбирает из общего пула только мобильные прокси"""
    x = json.loads(api_obj)
    id_pack = x['packages'].keys()
    mobile_pack = []

    for id in id_pack:
        name = x['packages'][id]['name']
        ip = x['packages'][id]['ips']
        address = ip[0].split(':')[0]
        port = ip[0].split(':')[1]
        if len(name.split(',')) > 2:
            mobile_pack.append([name, address, port])
    mobile_pack.sort(key=lambda i: i[0])
    return mobile_pack
