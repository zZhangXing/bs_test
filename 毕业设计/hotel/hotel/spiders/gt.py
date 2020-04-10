# -*- coding: utf-8 -*-
import scrapy
import json
from copy import deepcopy
import time
from hotel.items import GtItem


class GtSpider(scrapy.Spider):
    name = 'gt'
    allowed_domains = ['ihotel.meituan.com',
                       'hotel.meituan.com']
    t = time.strftime("%Y%m%d")
    start_urls = ['https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=touch&version_name=999.9&platformid=1&cateId=20&newcate=1&limit=20&offset=0&cityId=20&ci=20&startendday={0}~{0}&startDay={0}&endDay={0}&mypos=22.881382%2C113.997414&attr_28=129&sort=defaults&userid=614539654&uuid=4D4A3BC88E34AFAAAF47394F83B066326939811265CCE3F15EAB302A8639A3C0&lat=22.881382&lng=113.997414&accommodationType=1'.format(t)]

    def parse(self, response):
        id_li = json.loads(response.body)["query_ids"]
        if len(id_li) > 1:
            id = id_li[0]["position_id"]
            data_li = json.loads(response.body)["data"]["searchresult"]
            # print(response.request.headers['User-Agent'])
            item = GtItem()

            for data in data_li:
                item["name"] = data["name"]
                item["addr"] = data["addr"]
                item["price"] = data["lowestPrice"]
                item["score"] = data["avgScore"]
                item["poiId"] = data["poiid"]
                item["url"] = "https://hotel.meituan.com/{}".format(item["poiId"])
                # 获取position_id
                for i in id_li:
                    if item["poiId"] == i["poiId"]:
                        item["h_id"] = i["position_id"]


                # 评论
                # h_poiId = data["poiid"]

                url = "https://ihotel.meituan.com/api/v2/comments/biz/reviewList?referid={}&limit=15&start=0&filterid=800&querytype=1&utm_medium=touch&version_name=999.9".format(item["poiId"])
                time.sleep(2)
                yield scrapy.Request(
                    url,
                    callback=self.parse_hotel_comment,
                    meta={"item":deepcopy(item)}
                )

            # 翻页
            id = str(int(id) + 20)
            next_url = "https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=touch&version_name=999.9&platformid=1&cateId=20&newcate=1&limit=20&offset={0}&cityId=20&ci=20&startendday={1}~{1}&startDay={1}&endDay={1}&mypos=22.881382%2C113.997414&attr_28=129&sort=defaults&userid=614539654&uuid=4D4A3BC88E34AFAAAF47394F83B066326939811265CCE3F15EAB302A8639A3C0&lat=22.881382&lng=113.997414&accommodationType=1".format(id,self.t)
            # print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )


    def parse_hotel_comment(self,response):
        item = response.meta["item"]
        data_li = json.loads(response.body)["Data"]["List"]
        # print(data_li)
        comment = []
        for data in data_li:
            comment.append(data["Content"])
        item["comment"] = comment
        # 酒店详情

        yield scrapy.Request(
            item["url"],
            callback=self.parse_hotel_details,
            meta={"item": deepcopy(item)}
        )
        # print(item)

    def parse_hotel_details(self,response):
        item = response.meta["item"]
        item["details"] = response.xpath("//div[@class='poi-hotelinfo-content clearfix']/div[position()=3]/dd/span/text()").extract_first()
        # yield item
        # 图片
        yield scrapy.Request(
            "https://ihotel.meituan.com/group/v1/poi/{}/imgs?utm_medium=touch&version_name=999.9&platformid=1&classified=true".format(
                item["poiId"]),
            callback=self.parse_hotel_img,
            meta={"item": deepcopy(item)}
        )

    def parse_hotel_img(self,response):
        item = response.meta["item"]
        data_list = json.loads(response.body)["data"][:2]
        img_url_list = []
        imgs = []
        # print(data_list)
        for i in data_list:
            img_url_list.append(i["imgs"][0]["urls"])
        for i in img_url_list:
            for j in i:
                j = j.replace("w.h", "200.0.0")
                imgs.append(j)
        item["imgs"] = imgs
        yield item