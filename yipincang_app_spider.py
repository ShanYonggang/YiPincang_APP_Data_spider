import json
from mitmproxy import ctx
import pymongo

def response(flow):
    # 连接Mongodb数据库
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myClient['yipincang_goods_info']
    banner_collection = db['banner_info']
    goods_collection = db['goods_info']
    response = flow.response
    request = flow.request
    # app首页链接
    homeIndexUrl = 'http://ypc.gongchangtemai.com/shop/homev5/homeindex'
    goodList = 'http://ypc.gongchangtemai.com/shop/homev5/goodslist'
    # 获取主页每个品牌的基本信息
    if homeIndexUrl in request.url:
        text = response.text
        homeData = json.loads(text)
        bannersList = homeData.get('data').get('activity_list')
        for bannerInfo in bannersList:
            bannerData = {
                'bannerId': bannerInfo.get('activity_id'),
                'bannerImage': bannerInfo.get('activity_pic'),
                'bannerIntroduce': bannerInfo.get('ac_desc'),
                'endTime': bannerInfo.get('datetime')
            }
            ctx.log.error(str(bannerData))
            banner_collection.insert_one(bannerData)
    # 获取品牌内的商品信息
    if goodList in request.url:
        text = response.text
        goodData = json.loads(text)
        goodsList = goodData.get('data').get('goods_list')
        bannerID = goodData.get('data').get('activity_info').get('activity_id')
        for list in goodsList:
            goodStorage = list.get('goods_storage')
            if goodStorage != 0:
                good_data = {
                    'belongToBannerId': bannerID,
                    'goodImage': list.get('goods_image'),
                    'goodStorage': list.get('goods_storage'),
                    'goodMarketPrice':  list.get('goods_marketprice'),
                    'goodPrice': list.get('goods_price'),
                    'goodSize': list.get('size'),
                    'goodIntroduce': list.get('strace_title')
                }
                ctx.log.error(str(good_data))
                goods_collection.insert_one(good_data)