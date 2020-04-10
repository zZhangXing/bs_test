# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from models.es_types import GtType

from elasticsearch_dsl.connections import connections
es = connections.create_connection(GtType._doc_type.using)

def gen_suggests(index,info_tuple):
    #根据字符串生成搜索建议数组
    # "python重要性"  "title"
    # "python重要性"  "tags"
    used_words = set()
    suggests = []
    for text,weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index,analyzer="ik_max_word",params={"filter":["lowercase"]},body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})
    return suggests



class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GtItem(scrapy.Item):
    name = scrapy.Field()
    addr = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    comment = scrapy.Field()
    poiId = scrapy.Field()
    h_id = scrapy.Field()
    url = scrapy.Field()
    details = scrapy.Field()
    imgs = scrapy.Field()

    def save_to_es(self):
        hotel = GtType()
        hotel.name = self["name"]
        hotel.addr = self["addr"]
        hotel.score = self["score"]
        hotel.price = self["price"]
        hotel.comment = self["comment"]
        hotel.poiId = self["poiId"]
        hotel.h_id = self["h_id"]
        hotel.url = self["url"]
        hotel.details = self["details"]
        hotel.imgs = self["imgs"]
        hotel.suggest = gen_suggests(GtType._doc_type.index, ((hotel.name,10),(hotel.addr,7)))

        hotel.save()

        return