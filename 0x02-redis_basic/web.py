#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of the function
is very simple. It uses the requests module to obtain the HTML content
of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code written in
exercise.py.

Inside get_page track how many times a particular URL was accessed in the key
"count:{url}" and cache the result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and
test your caching.
"""
from redis import Redis
import requests
from typing import Callable
from functools import wraps

redis = Redis()


def call_count(method: Callable) -> Callable:
    """Counts how many times a function is called"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """wraps the method"""
        redis = redis.Redis()
        key = f"count:{args[0]}"
        redis.incr(key, 1)
        redis.expire(key, 10)
        return method(*args, **kwargs)
    return wrapper


def get_page(url: str) -> str:
    """Obtains the HTML content of a particular URL
    and returns it
    Args:
        url (str): a url string
    Returns:
        (str): the HTML content of the url
    """
    get = call_count(requests.get)
    req = get(url)
    return req.text
