# coding:utf8
import requests
from requests.cookies import cookiejar_from_dict
import time


class Req_s(object):
    """docstring for req_s"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }

    def __init__(self, keep_alive=True, headers=None, cookies_dic=None, DEFAULT_RETRIES=3):
        super(Req_s, self).__init__()
        req_s = requests.Session()

        req_s.keep_alive = keep_alive
        req_s.headers = headers or self.__class__.headers

        cookies_dic = cookies_dic or {}
        req_s.cookies = cookiejar_from_dict(cookies_dic)

        req_s.adapters.DEFAULT_RETRIES = DEFAULT_RETRIES

        self.req_s = req_s

    def __getattr__(self, attr):
        if attr == "req_s":
            return getattr(self, attr)
        else:
            return getattr(self.req_s, attr)


    @classmethod
    def get_bycls(cls, url):
        req_s = requests.Session()
        req_s.adapters.DEFAULT_RETRIES = 3
        req_s.keep_alive = False
        req_s.headers = cls.headers
        req_s.cookies = cookiejar_from_dict({})
        return req_s.get(url)




if __name__ == '__main__':
    a = Req_s()
    a.get("http://www.baidu.com")
