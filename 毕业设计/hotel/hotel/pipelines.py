# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from models.es_types import GtType
from hotel.items import GtItem


class HotelPipeline(object):
    def __init__(self):
        self.file = codecs.open(filename='hotel.csv', mode='w+', encoding='utf-8')

    def process_item(self, item, spider):
        res = dict(item)
        # 如果直接将字典形式的数据写入文件，会发生错误
        # 所以需要将字典形式的值，转化成字符串 写入到文件当中
        st = json.dumps(res, ensure_ascii=False)
        self.file.write(st)
        self.file.write(',\n')
        return item

    def open_spider(self,spider):
        pass

    def close_spider(self, spider):
        self.file.close()


class ElasticsearchPipeline(object):
    # 将数据写入到es中

    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()
        return item
