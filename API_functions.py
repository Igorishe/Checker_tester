import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

auth_id = os.getenv('AUTH_ID')
auth_key = os.getenv('AUTH_KEY')
api_host = os.getenv('API_HOST')


def get_proxies_by_api():
    """Получает все пакеты по API"""
    headers = {
        'X-Auth-ID': auth_id,
        'X-Auth-Key': auth_key
    }
    response = requests.post(
        api_host,
        headers=headers,
        data=''
    )
    return response.text


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
