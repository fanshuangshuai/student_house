# coding=utf-8
import functools
import time

from others.codeLearning.cacheLearning.my_lrucache import LRUCacheDict

CACHE = {}

def time_it(func):
    """计算函数执行时间的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(func.__name__, ' functions execute ', time.time() - start, ' s')
    return wrapper

@time_it
def test():
    time.sleep(5)

# test()

# def passiveQuery(sql):
#     """被动缓存，有异常判断，开销较大"""
#     try:
#         result = CACHE[sql]         # 从cache中取值，取不到的话就放进去，取到的话就return。
#     except KeyError:
#         print('run except')
#         time.sleep(1)
#         result = 'execute %s' % sql
#         CACHE[sql] = result
#     return result
#
#
# def passive2Query(sql):
#     """被动缓存，没有异常判断，开销较少"""
#     result = CACHE.get(sql)
#     if not result:
#         time.sleep(1)
#         result = 'execute %s' % sql
#         CACHE[sql] = result
#     return result
#
# # 缓存装饰器
# def cache_it(func):
#     @functools.wraps(func)      # 保留原函数的签名（所有属性）
#     def inner(*args, **kwargs):
#         key = repr(*args, **kwargs)     # repr 把传递给它的对象都转为字符串
#         try:
#             result = CACHE[key]
#         except KeyError:
#             result = func(*args, **kwargs)
#             CACHE[key] = result
#         return result
#     return inner


# 增强缓存装饰器
def enchanceCache_it(max_size=1024, expiration=60):
    CACHE = LRUCacheDict(max_size=max_size, expiration=expiration)

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            try:
                result = CACHE[key]
            except KeyError:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result
        return inner
    return wrapper

# 正常的业务逻辑
# @cache_it
# def query(sql):
#     time.sleep(2)
#     result = 'execute %s' % sql
#     return result

@time_it
@enchanceCache_it(max_size=10, expiration=3)
def query(sql):
    time.sleep(1)
    result = 'execute %s' % sql
    return result


if __name__ == '__main__':
    query('select * from blog_post')
    query('select * from blog_post')