# coding=utf-8
import time
from collections import OrderedDict


class LRUCacheDict:
    def __init__(self, max_size=1024, expiration=60):
        """最大容量为1024个key，每个key的有效期是60s"""
        self.max_size = max_size
        self.expiration = expiration

        self._cache = {}
        self._access_records = OrderedDict()    # 记录访问时间
        self._expire_records = OrderedDict()    # 记录失效时间

    def __setitem__(self, key, value):
        """data load cache：
        1. 删除cache中以前的key（更新cache）
        2. 设置key的失效时间、访问时间
        3. 清理cache
        """
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._expire_records[key] = now + self.expiration
        self._access_records[key] = now

        self.cleanup()

    def __getitem__(self, key):
        """get cache
        1. 更新key的访问时间
        2. 清理cache
        3. 返回key
        """
        now = int(time.time())
        del self._access_records[key]
        self._access_records[key] = now
        self.cleanup()

        return self._cache[key]

    def __contains__(self, key):
        """判断缓存中是否有key
        1. 清理cache
        2. 返回 TRUE or False
        """
        self.cleanup()
        return key in self._cache

    def __delete__(self, key):
        """删除cache中的key
        1. 删除cache中的key
        2. 删除key的访问时间、失效时间
        """
        if key in self._cache:
            del self._cache[key]
            del self._expire_records[key]
            del self._access_records[key]

    def cleanup(self):
        """去掉无效（过期或者超出存储大小）的缓存"""
        if self.expiration is None:
            return None

        pending_delete_keys = []
        now = int(time.time())
        # 删除已经过期的cache
        for k, v in self._expire_records.items():
            if v < now:
                pending_delete_keys.append(k)

        for del_k in pending_delete_keys:
            self.__delete__(del_k)

        # 如果数据量大于max_size，则删掉最旧的cache
        while len(self._cache) > self.max_size:
            # 删除最先访问的key，因为_access_records是有序的
            for k in self._access_records:
                self.__delete__(k)
                break

if __name__ == '__main__':
    cache_dict = LRUCacheDict(max_size=2, expiration=10)
    cache_dict['name'] = 'Fnanshan'
    cache_dict['age'] = 30
    cache_dict['addr'] = 'tianjin'

    print('name' in cache_dict) # False
    print('age' in cache_dict)  # True
    time.sleep(11)
    print('age' in cache_dict)  # False