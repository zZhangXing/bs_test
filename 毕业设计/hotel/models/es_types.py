# -*- coding: utf-8 -*-
"""
file: es_types.py
data: 2020-02-28-0:08
author: zhang
"""
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text,Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word",filter=["lowercase"])


class GtType(DocType):

    suggest = Completion(analyzer=ik_analyzer)
    name = Text(analyzer="ik_max_word")
    addr = Text(analyzer="ik_max_word")
    price = Integer()
    score = Integer()
    details = Text(analyzer="ik_max_word")
    comment = Text(analyzer="ik_max_word")
    poiId = Integer()
    h_id = Integer()
    url = Keyword()
    imgs = Keyword()

    class Meta:
        index = "gt"
        doc_type = "meituan"

if __name__ == "__main__":
    GtType.init()