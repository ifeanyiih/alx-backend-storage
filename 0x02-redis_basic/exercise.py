#!/usr/bin/env python3
"""Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the
input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float
"""
from typing import Union
from uuid import uuid4
from redis import Redis


class Cache:
    """Stores an instance of Redis client
    as a private variable and has methods to perform
    operations on a Redis server

    Attributes:
        _redis (Redis client instance): client instance
    """
    def __init__(self) -> None:
        """Initializes the class and creates
        the redis instance"""
        self._redis: Redis = Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in a Redis data base using a
        randomly generated key, returns the key

        Args:
            data (Union[str, bytes, int, float]): data
        Returns:
            (str): the generated key
        """
        if type(data) not in [str, bytes, int, float]:
            return None
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key
