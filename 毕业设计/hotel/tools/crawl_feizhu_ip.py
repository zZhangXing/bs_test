# -*- coding: utf-8 -*-
"""
file: crawl_feizhu_ip.py
data: 2020-03-11-13:49
author: zhang
"""
import requests
from scrapy.selector import Selector

def crawl_ips():
    re = requests.get("http://120.79.85.144/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=10&time=1&port=1&format=txt&ss=1&css=&pro=&city=&dt=0&usertype=20").text

    ip_list = re.split("\r\n")
    i_list = []
    ip_dict = {}
    print(ip_list)
    for i in ip_list:
        # print(type(i))
        ip = i.split(":")[0]
        port = i.split(":")[-1]
        print(ip,port)



if __name__ == '__main__':
    crawl_ips()