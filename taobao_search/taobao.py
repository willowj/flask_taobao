
# coding:utf8

from request import Req_s
from parase import Crawler, CrawlerError
from clean_filter import Result

goods_unite = {}



def unite_goods(good_name=None, only_tmall='',
                         price_min=None,
                         price_max=None,
                         keyword=None,
                         descripHrequ=0,
                         servHrequ=0,
                         threshold_count=None):
    Result.results = []
    z = set()
    print str(good_name == u'男外套')
    print good_name in goods_unite

    for item in goods_unite[good_name]:
        if item['detail_url'] not in z:
            z.add(item['detail_url'])
            Result.results.append(item)

    Result.filter(keyword=keyword, comment_count=threshold_count,descripHrequ=descripHrequ, servHrequ=servHrequ)

    Result.results.sort(key=lambda x: x['rate'], reverse=True)

    return Result.results

def search_filter_taobao(good_name=None, only_tmall='',
                         price_min=None,
                         price_max=None,
                         keyword=None,
                         descripHrequ=0,
                         servHrequ=0,
                         threshold_count=None,
                         start_page=0):
    print "--"*30
    print locals()
    print "--"*30
    if good_name is None:
        return []

    ses = Req_s()

    initial_url = 'https://s.taobao.com/search?q=' + \
        good_name + '&_input_charset=utf-8'

    if only_tmall is not None and only_tmall.lower() == 'on':
        initial_url = initial_url + '&filter_tianmao=tmall'

    if price_min:
        if float(price_min) < float(price_max):
            initial_url = initial_url+'&filter=reserve_price%5B' + \
                '%s' % price_min+'%2C' + '%s' % price_max

    initial_url = initial_url + '&cd=false&sort=renqi-desc&%5D&s='
    Result.results = []

    # z = ses.get(initial_url)
    # raw_data = Crawler.crawl_data(z.text)
    # Result.exten_resu(raw_data)

    t = 0
    while t < 2:
        next_url = initial_url+str(44*(t+start_page))

        z = ses.get(next_url)

        if not (200<= z.status_code <305):
            raise CrawlerError("status_code%d"%z.status_code)

        raw_data = Crawler.crawl_data(z.text)
        Result.exten_resu(raw_data)

        t += 1
        if len(raw_data) < 30:
            next_t = "#"
            break
        next_t = t+start_page

    Result.product_rank_all()

    Result.filter(keyword=keyword, comment_count=threshold_count,descripHrequ=descripHrequ, servHrequ=servHrequ)
    Result.results.sort(key=lambda x: x['rate'], reverse=True)

    try:
        goods_unite[good_name].extend(Result.results)
    except ( AttributeError, KeyError):
        goods_unite[good_name] = Result.results
    print len(goods_unite),len(goods_unite[good_name]),u'男外套' in goods_unite

    print "t", next_t
    return Result.results, next_t
