# coding:utf8
import re
import json

class Crawler(object):
    """docstring for get_data"""
    total_count = None
    total_page = None
    current_page = None
    #get_googs = 0

    def __init__(self, arg=None):
        super(get_data, self).__init__()
        self.arg = arg

    @classmethod
    def get_totalCount(cls, page_source):
        # print 'code:', code
        reg = '"pageSize":[0-9]*?,"totalPage":([0-9]*?),"currentPage":([0-9]*?),"totalCount":([0-9]*?)}'
        re_f = re.findall(reg, page_source)
        if re_f:
            re_f = re_f[0]
        else:
            return None
        cls.total_page = int(re_f[0])
        cls.current_page = int(re_f[1])
        cls.total_count = int(re_f[2])

    @classmethod
    def crawl_data(cls, page_source):
        cls.get_totalCount(page_source)
        re_p = '"auctions":([\s\S]*),"recommendAuctions"'
        pat = re.compile(re_p)
        meet_code = re.findall(pat, page_source)
        if len(meet_code)<1:
            raise CrawlerError('page_source_finds_none')
        raw_data = json.loads(meet_code[0])
        return raw_data


class CrawlerError(TypeError):
    """docstring for CrawlerError"""
    def __init__(self,*arg):
        super(CrawlerError, self).__init__(*arg)

