# -*- coding: utf-8 -*-
"""
file: a.py
data: 2020-03-09-22:57
author: zhang
"""
import redis
redis_cli = redis.StrictRedis()
a = 1
redis_cli.zincrby("search_keywords_set",-1,a)