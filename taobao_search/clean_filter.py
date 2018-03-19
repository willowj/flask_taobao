# coding=utf8
import sys

from math import log
# import urllib


py3 = sys.version_info[0]==3

keyword = None

descripHrequ = None
servHrequ = None
comment_count = None



class Result(object):
    """docstring for Results"""
    results = []
    av_price = None
    av_dscrp = None

    def __init__(self, arg):
        super(Results, self).__init__()
        self.arg = arg

    @classmethod
    def exten_resu(cls, raw_data):
        cls.clean_data(raw_data)
        cls.results.extend(raw_data)

    @classmethod
    def clean_data(cls, data):
        for i, item in enumerate(data):
            if 'p4pSameHeight' in item:
                data.pop(i)
        for x in data:
            cls.item_clean(x)

    @staticmethod
    def item_clean(item):

        if 'i2iTags' in item:
            item.pop('i2iTags')
        if 'p4pTags' in item:
            item.pop('p4pTags')
        if 'icon' in item:
            item.pop('icon')

        item['view_price'] = float(item['view_price'])
        item['view_fee'] = float(item['view_fee'])
        item['view_sales'] = int(item['view_sales'].replace(u'人付款', ''))

        item['comment_count'] = item['comment_count'] and int(
            item['comment_count']) or 0

        item['user_id'] = int(item['user_id'])

        item['shop_classN'] = len(item['shopcard']['levelClasses'])

        item['shop_class'] = item['shop_classN'] and item['shopcard'][
            'levelClasses'][0]['levelClass'][-4:] or ''

        item['isTmall'] = item['shopcard']['isTmall']

        item['delivery0'] = float(item['shopcard']['delivery'][0])/100
        item['delivery_h'] = float(item['shopcard']['delivery'][1]) * \
            float(item['shopcard']['delivery'][2])/100

        item['description0'] = float(item['shopcard']['description'][0])/100
        item['description_h'] = float(item['shopcard']['description'][1]) * \
            float(item['shopcard']['description'][2])/100

        item['service0'] = float(item['shopcard']['service'][0])/100
        item['service_h'] = float(item['shopcard']['service'][1]) * \
            float(item['shopcard']['service'][2])/100

        item['encryptedUserId'] = item['shopcard']['encryptedUserId']
        item['sellerCredit'] = item['shopcard'].get('sellerCredit', 0)
        item['totalRate'] = item['shopcard'].get('totalRate', 0)

        item.pop('shopcard')
        item.pop('title')

    @staticmethod
    def recommend_rate(item, av_price, av_dscrp):
        # 描述为绝对值
        rate = (item['description0']/av_dscrp)**20  \
            * (item['description0'] + item['delivery0'] + item['service0']) \
            * (av_price/(item['view_price']))**0.1 \
            + log((item['comment_count']+5), 1000)
        return rate

    @classmethod
    def product_rank_all(cls):
        Gn = len(cls.results)
        if Gn and (not cls.av_price or not cls.av_dscrp):
            cls.av_price = sum(v["view_price"] for v in cls.results) / Gn
            cls.av_dscrp = sum(v["description0"] for v in cls.results) / Gn

        for item in cls.results:
            item['rate'] = cls.recommend_rate(item, cls.av_price, cls.av_dscrp)

    @staticmethod
    def fliter_f(item, keyword=None, descripHrequ=None, servHrequ=None, comment_count=None):
        if keyword and keyword not in item['raw_title']:
            return False
        if descripHrequ is not None and descripHrequ > item['description_h']:
            return False
        if servHrequ is not None and servHrequ > item['service_h']:
            return False
        if comment_count is not None and comment_count > item['comment_count']:
            return False
        # print "fliter_f,descripHrequ",descripHrequ
        return True

    @classmethod
    def filter(cls,keyword=None, descripHrequ=None, servHrequ=None, comment_count=None):
        # print "filter,descripHrequ",descripHrequ
        cls.results = filter(lambda x: cls.fliter_f(
            x, keyword=keyword, descripHrequ=descripHrequ, servHrequ=servHrequ, comment_count=comment_count),
            cls.results)
        if py3:
            cls.results = list(cls.results)

        # print "filter",comment_count

if __name__ == '__main__':

    from browser import Crawler
    raw_data = Crawler.crawl_data(z.text)
    # Result.clean_data(raw_data)
    Result.exten_resu(raw_data)

    Result.product_rank_all()
    Result.filter()
    Result.results.sort(key=lambda x: x['rate'], reverse=True)

    serchProd = u'羽绒服'
    save(Result, serchProd, savePath=None)
