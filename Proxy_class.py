import requests

class MobProxy:
    def __init__(self, ip, port, country, city, isp, auth, status):
        self.ip = ip
        self.port = port
        self.country = country
        self.city = city
        self.isp = isp
        self.auth = auth
        self.status = status

    def get_proxies(file):
        f = open(file, 'r')
        proxy_list = f.readlines()
        f.close()
        for i in range(len(proxy_list)):
            proxy_list[i] = proxy_list[i].replace("\n", "")
        return proxy_list

    def check_status(proxy):
        r = requests.get('http://2ip.ru/', proxies={"http": "http://{}@{}:{}".format(proxy.auth, proxy.ip, proxy.port),
                                                    "https": "https://{}@{}:{}".format(proxy.auth, proxy.ip, proxy.port)})
        proxy.status = r.status_code