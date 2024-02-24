"""
File: BaseStation.py
Author: Doraemon
Description: 基站类
"""
from collections import OrderedDict
from decimal import Decimal
from functools import wraps
from threading import RLock
import time
import typing as t
from Constant import *
import sys
import Constant


F = t.TypeVar("F", bound=t.Callable[..., t.Any]) # 函数类型，参数为任意，返回值为任意
T_DECORATOR = t.Callable[[F], F] # 函数类型，参数为F，返回值为F
T_TTL = t.Union[int, float] # int或float类型的联合体

class BaseStation:
    """
    An in-memory, FIFO cache object.

    It supports:

    - Maximum number of cache entries
    - Global TTL default
    - Per cache entry TTL
    - TTL first/non-TTL FIFO cache eviction policy

    Cache entries are stored in an ``OrderedDict`` so that key ordering based on the cache type can
    be maintained without the need for additional list(s). Essentially, the key order of the
    ``OrderedDict`` is treated as an "eviction queue" with the convention that entries at the
    beginning of the queue are "newer" while the entries at the end are "older" (the exact meaning
    of "newer" and "older" will vary between different cache types). When cache entries need to be
    evicted, expired entries are removed first followed by the "older" entries (i.e. the ones at the
    end of the queue).

    Attributes:
        maxsize: Maximum size of cache dictionary. Defaults to ``256``.
        ttl: Default TTL for all cache entries. Defaults to ``0`` which means that entries do not
            expire. Time units are determined by ``timer`` function. Default units are in seconds.
        timer: Timer function to use to calculate TTL expiration. Defaults to ``time.time`` where
            TTL units are in seconds.
        default: Default value or function to use in :meth:`get` when key is not found. If callable,
            it will be passed a single argument, ``key``, and its return value will be set for that
            cache key.
    """
    """
    成员变量：
    - id: 基站的id
    - x: x坐标
    - y: y坐标
    - maxsize: 缓存容量(按数量算)
    - radius: 覆盖半径
    - storeCost: 存储成本
    - transmissionRate: 传输速率
    - _cache: 缓存的内容
    - users: 服务的用户id
    - maxsize: 缓存容量
    """
    _cache: OrderedDict
    _expire_times: t.Dict[t.Hashable, T_TTL]
    _lock: RLock

    def __init__(
        self,
        id: int,
        x: int,
        y: int,
        maxsize: int = CACHECAPACITY,
        ttl: T_TTL = 0,
        timer: t.Callable[[], T_TTL] = time.time,
    ):
        self.id = id
        self.x, self.y = x, y
        self.maxsize = maxsize
        self.ttl = ttl
        self.timer = timer
        self.radius = RADIUS
        self.storeCost = STORECOST
        self.transmissionRate = TRANSTIME

        self.setup()
        self.configure(maxsize=maxsize, ttl=ttl, timer=timer)

    def setRadius(self, radius):
        self.radius = radius
    
    def setstrCost(self, storeCost):
        self.storeCost = storeCost
    
    def setTransimissionRate(self, transmissionRate):
        self.transmissionRate = transmissionRate

    def addUser(self, user):
        if(user in self.users):
            print("用户已存在")
            return
        self.users.append(user)
    
    def printUsers(self):
        print(f'id: {id}')
        for user in self.users:
            print(user.id, end=' ')
        print()

    def setup(self) -> None:
        self._cache: OrderedDict = OrderedDict()
        self._expire_times: t.Dict[t.Hashable, T_TTL] = {}
        self.users = []
        self._lock = RLock()

    def configure(
        self,
        maxsize: t.Optional[int] = None,
        ttl: t.Optional[T_TTL] = None,
        timer: t.Optional[t.Callable[[], T_TTL]] = None,
    ) -> None:
        if maxsize is not None:
            if not isinstance(maxsize, int):
                raise TypeError("maxsize must be an integer")

            if not maxsize >= 0:
                raise ValueError("maxsize must be greater than or equal to 0")

            self.maxsize = maxsize

        if ttl is not None:
            if not isinstance(ttl, (int, float, Decimal)):
                raise TypeError("ttl must be a number")

            if not ttl >= 0:
                raise ValueError("ttl must be greater than or equal to 0")

            self.ttl = ttl

        if timer is not None:
            if not callable(timer):
                raise TypeError("timer must be a callable")

            self.timer = timer

    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: t.Hashable) -> bool:
        return self.has(key)

    def copy(self) -> OrderedDict:
        with self._lock:
            return self._cache.copy()

    def keys(self) -> t.KeysView:
        return self.copy().keys()

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._expire_times.clear()

    def has(self, key: t.Hashable) -> bool:
        with self._lock:
            return key in self._cache

    def size(self) -> int:
        return len(self)

    def full(self) -> bool:
        if self.maxsize is None or self.maxsize <= 0:
            return False
        return len(self) >= self.maxsize

    def add(self, key: t.Hashable, ttl: t.Optional[T_TTL] = 0) -> None:
        with self._lock:
            if self.has(key):
                if Constant.DEBUG_ON:
                    print(f'已经存在{key}')
                return
            if self.full():
                if Constant.DEBUG_ON:
                    print('缓存已满')
                self.evict()
            self._cache[key] = True
            if(ttl != 0):
                self._expire_times[key] = self.timer() + ttl
            else:
                self._expire_times[key] = sys.maxsize # 永不过期
            if Constant.DEBUG_ON:
                print(f'基站：{self.id} | 缓存：{key}')
        

    def delete(self, key: t.Hashable) -> int:
        with self._lock:
            count = 0
            try:
                del self._cache[key]
                count = 1
            except KeyError:
                pass

            try:
                del self._expire_times[key]
            except KeyError:
                pass

            return count
        
    # 删除过期的元素
    def delete_expired(self):
        with self._lock:
            expires_on = self.timer()
            expire_times = self._expire_times.copy()

            for key, expiration in expire_times.items():
                if expiration <= expires_on:
                    self.delete(key)

    # 缓存替换
    def evict(self):
        self.delete_expired()
        if not self.full():
            return
        with self._lock:
            self.popitem()

    # 删除第一个元素
    def popitem(self) -> t.Tuple[t.Hashable, t.Any]:
        with self._lock:
            first_key = next(iter(self._cache))
            if Constant.DEBUG_ON:
                print(f'基站：{self.id} | 删除：{first_key}')
            self.delete(first_key)