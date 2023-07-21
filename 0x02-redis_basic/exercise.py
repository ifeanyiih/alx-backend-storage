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


Familiarize yourself with redis commands RPUSH, LPUSH, LRANGE, etc.

In this task, we will define a call_history decorator to store the history
of inputs and outputs for a particular function.

Everytime the original function will be called, we will add its input
parameters to one list in redis, and store its output into another list.

In call_history, use the decorated function’s qualified name and append
":inputs" and ":outputs" to create input and output list keys, respectively.

call_history has a single parameter named method that is a Callable and returns
a Callable.

In the new function that the decorator will return, use rpush to append the
input arguments. Remember that Redis can only store strings, bytes and numbers.
Therefore, we can simply use str(args) to normalize. We can ignore potential
kwargs for now.

Execute the wrapped function to retrieve the output. Store the output using
rpush in the "...:outputs" list, then return the output.

Decorate Cache.store with call_history

************************

mplement a replay function to display the history of calls of a particular
function.

Use keys generated in previous tasks to generate the following output
"""
from typing import Union, Callable, Optional
from functools import wraps
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """Takes a functiona s parameter and
    returns a function. It counts how many times methods
    of Cache class are called"""
    @wraps(method)
    def wrapper(self, *args: list, **kwds: dict) -> None:
        """Increments the count for key f.__qualname__
        every time method is called"""
        self._redis.incr(method.__qualname__, 1)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a
    particular function
    Args:
        method (a python method)
    Returns:
        returns a function (method) in this case
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> None:
        """A wrapper function for decorating the method"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))
        return output
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
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


def replay(method: Callable) -> None:
    """Display the history of calls of a particular
    function
    Args:
        method : a python class method
    """
    redis_ = redis.Redis()
    print(f"{method.__qualname__} was called "
          f"{int(redis_.get(method.__qualname__))} times:")
    history = zip(redis_.lrange(f"{method.__qualname__}:inputs", 0, -1),
                  redis_.lrange(f"{method.__qualname__}:outputs", 0, -1))
    for key, val in history:
        key_dec = key.decode('utf-8')
        val_dec = val.decode('utf-8')
        print(f"{method.__qualname__}(*{key_dec}) -> {val_dec}")
