# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask, flash, redirect, render_template, \
    request, Response, make_response, session, url_for, jsonify


from taobao_search import search_filter_taobao, unite_goods
from taobao_search import CrawlerError

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/search_good', methods=['POST'])
def search_good():
    # return str(request.form)

    searchgoods = request.form.get('searchgoods', None)
    min_price = request.form.get('min_price', None)
    max_price = request.form.get('max_price', None)
    only_tmall = request.form.get('only_tmall', None)
    keyword = request.form.get('keyword', None)

    threshold_count = request.form.get('threshold_count', None)
    threshold_count = int(threshold_count) if threshold_count else None

    descripHrequ = request.form.get('descripHrequ', 0)
    descripHrequ = float(descripHrequ) if descripHrequ else 0

    servHrequ = request.form.get('servHrequ', 0)
    servHrequ = float(servHrequ) if servHrequ else 0

    print request.form
    if not searchgoods:
        flash(u"搜索商品不能为空", 'info')
        return redirect(url_for('index'))
    else:
        serch_info = dict(good_name=searchgoods,
                          only_tmall=only_tmall,
                          price_min=min_price,
                          price_max=max_price,
                          keyword=keyword,
                          threshold_count=threshold_count,
                          descripHrequ=descripHrequ,
                          servHrequ=servHrequ
                          )
        session.update(serch_info=serch_info)

        # return jsonify(serch_info)
        try:
            results, next_t = search_filter_taobao(**serch_info)
        except CrawlerError as e:
            return str(e)+u"\n 请尝试刷新"

        print serch_info, "\nnext_t", next_t
        return render_template("items.html",
                               results=results,
                               serch_info=serch_info,
                               next_t=next_t,
                               good_name=serch_info["good_name"].encode('utf8')
                               )


@app.route('/next_t/<int:start_page>')
def next_t(start_page=1):
    print dir(session)
    print session
    # print request.data
    serch_info = session["serch_info"]
    serch_info["start_page"] = start_page

    try:
        results, next_t = search_filter_taobao(**serch_info)
    except CrawlerError as e:
        return str(e) + u"\n请求不要过快，以免淘宝反爬虫， 请尝试刷新"

    print serch_info["good_name"]
    return render_template("items.html",
                           results=results,
                           serch_info=serch_info,
                           next_t=next_t,
                           good_name=serch_info["good_name"].encode('utf8')
                           )




@app.route('/unite/<goods_name>')
def unite(goods_name):
   #  return str(goods_name == u'男外套')
    # try:
    serch_info = session["serch_info"]
    results = unite_goods(**serch_info)
    # except (AttributeError, KeyError):
    #     flash(u'没有搜索过该商品 请先搜索浏览')
    #     return redirect(url_for('index'))
    # else:
    return render_template("items.html",
                           results=results,
                           serch_info=session['serch_info'],
                           good_name=serch_info["good_name"]
                           )

@app.route('/')
def index():
    return render_template("items.html", serch_info={})


@app.route('/add_cookie')
def add_cookie():
    import time

    res = make_response('111111111')
    res.set_cookie('b',"333", expires=time.time()+6*60)
    return res

@app.route('/get_cookie')
def get_cookie():

    return request.cookies.get("b")


if __name__ == '__main__':
    app.run(debug=True, port=5004, threaded=True)
