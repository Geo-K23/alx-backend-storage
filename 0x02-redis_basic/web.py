#!/usr/bin/env python3
"""
A module with tools for request, caching and tracking
"""
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    """
    Uses the requests module to obtain the HTML content
    of a particular URL and returns it
    """
    r = redis.Redis()
    key = "count:{}{}{}".format('{', url, '}')
    r.incr(key)
    res = requests.get(url)
    r.setex(url, timedelta(seconds=10), res.text)
    return res.text
