#!/usr/bin/env python3
"""Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the
input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float


Redis only allows to store string, bytes and numbers (and lists thereof).
Whatever you store as single elements, it will be returned as a byte string.
Hence if you store "a" as a UTF-8 string, it will be returned as b"a" when
retrieved from the server.

In this exercise we will create a get method that take a key string argument
and an optional Callable argument named fn. This callable will be used to
convert the data back to the desired format.

Remember to conserve the original Redis.get behavior if the key does not exist.

Also, implement 2 new methods: get_str and get_int that will automatically
parametrize Cache.get with the correct conversion function.
"""
from typing import Union, Callable, Optional
from functools import wraps
from uuid import uuid4
import redis


def count_calls(f: Callable) -> Callable:
    """Takes a functiona s parameter and
    returns a function. It counts how many times methods
    of Cache class are called"""
    @wraps(f)
    def wrapper(*args: list, **kwds: dict) -> None:
        """Increments the count for key f.__qualname__
        every time method is called"""
        args[0]._redis.incr(f.__qualname__, 1)
        return f(*args, **kwds)

    return wrapper


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
        _redis: Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in a Redis data base using a
        randomly generated key, returns the key

        Args:
            data (Union[str, bytes, int, float]): data
        Returns:
            (str): the generated key
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes],
                         Union[str, bytes, int,
                                  float]]] = None) -> Union[str,
                                                            bytes, int, float]:
        """Gets a value from the redis store using the key
        and converts back to the type using the optional callable
        Args:
            key (str): key to get data with
            fn (function): an optional Callable
        Returns:
            returns data with required type or bytes type
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, value: bytes) -> str:
        """Converts the value to string type"""
        return str(value.decode('utf-8'))

    def get_int(self, value: bytes) -> int:
        """Converts the value to int type"""
        return int(value.decode('utf-8'))
