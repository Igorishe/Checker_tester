from requests import Request, Session
import json


def get_proxies_by_api():
    s = Session()
    headers = {
        'X-Auth-ID': '199',
        'X-Auth-Key': '1c8a8c80f01a33401057079b666f2825db3680fc187de61f7ebb99eba526ff88'
    }
    url = 'https://rsocks.net/api/v1/file/get-proxy'
    req = Request('POST', url, data='', headers=headers)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    return resp.text


def parse_data(api_obj):
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

    return mobile_pack

parse_data(get_proxies_by_api())
