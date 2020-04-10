import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import GtType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

redis_cli = redis.StrictRedis()

client = Elasticsearch(hosts=["127.0.0.1"])


class IndexView(View):
    # 首页
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        return render(request, "index.html", {"topn_search": topn_search})


# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = GtType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 1
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source["name"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")

        redis_cli.zincrby("search_keywords_set", 1, key_words)

        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1
        start_time = datetime.now()
        response = client.search(
            index="gt",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["name", "addr"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "highlight": {
                    "pre_tags": ["<span class='keyWord'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "name": {},
                        "addr": {}
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "name" in hit["highlight"]:
                hit_dict["name"] = "".join(hit["highlight"]["name"])
            else:
                hit_dict["name"] = hit["_source"]["name"]
            if "addr" in hit["highlight"]:
                hit_dict["addr"] = "".join(hit["highlight"]["addr"])
            else:
                hit_dict["addr"] = hit["_source"]["addr"]
            hit_dict["score"] = hit["_source"]["score"]
            hit_dict["price"] = hit["_source"]["price"]
            hit_dict["url"] = hit["_source"]["url"]
            if "details" in hit["_source"] :
                hit_dict["details"] = hit["_source"]["details"]
            else:
                hit_dict["details"] = "暂无详情"
            # hit_dict["comment"] = hit["_source"]["comment"][:3]
            hit_list.append(hit_dict)
            # print(hit_list)

        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "topn_search": topn_search,
                                               })
