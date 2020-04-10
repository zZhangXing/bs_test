# -*- coding: utf-8 -*-
"""
file: main.py
data: 2020-02-28-0:17
author: zhang
"""
from scrapy.cmdline import execute
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "gt"])