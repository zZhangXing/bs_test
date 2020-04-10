# -*- coding: utf-8 -*-
"""
file: ab.py
data: 2020-02-20-15:32
author: zhang
"""
import requests
from lxml import etree
import re
import json
import datetime
import time
from fake_useragent import UserAgent

# headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
# # response = requests.get("https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=touch&version_name=999.9&platformid=1&cateId=20&newcate=1&limit=20&offset=1080&cityId=20&ci=20&startendday=20200220~20200220&startDay=20200220&endDay=20200220&mypos=22.881382%2C113.997414&attr_28=129&sort=defaults&userid=614539654&uuid=4D4A3BC88E34AFAAAF47394F83B066326939811265CCE3F15EAB302A8639A3C0&lat=22.881382&lng=113.997414&accommodationType=1",headers=headers)
#
# # di = json.loads(response.text)
# # l = di["query_ids"]
# # print(l[0]["position_id"])
# # print(datetime.datetime.now().day)
# # t = time.strftime("%Y%m%d")
# # print(type(t),t)
# ua = UserAgent()
# for i in range(10):
#     print(ua.random)

# a = 24%10
# print(a)

url = "https://ihotel.meituan.com/group/v1/poi/195160614/imgs?utm_medium=touch&version_name=999.9&platformid=1&classified=true"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

a = requests.get(url=url, headers=headers).content.decode("utf-8")
a = json.loads(a)
item = {}
img_url_list = []
img = []
img_list = a["data"][:2]
print(img_list)
for i in img_list:
    # print(i)
    img_url_list.append(i["imgs"][0]["urls"])
for i in img_url_list:
    for j in i :
        j = j.replace("w.h","200.0.0")
        img.append(j)
item["img"] = img
print(item)

# u = 'http://p1.meituan.net/w.h/dnaimgdark/115645ae27d6285ff1c1575c25de9af39135148.jpg'
# u = u.replace("w.h", "200.0.0")
# print(u)