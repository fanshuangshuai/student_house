# coding=utf-8
import functools
import time

CACHE = {}

def passiveQuery(sql):
    """被动缓存，有异常判断，开销较大"""
    try:
        result = CACHE[sql]         # 从cache中取值，取不到的话就放进去，取到的话就return。
    except KeyError:
        print('run except')
        time.sleep(1)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result


def passive2Query(sql):
    """被动缓存，没有异常判断，开销较少"""
    result = CACHE.get(sql)
    if not result:
        time.sleep(1)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result

# 缓存装饰器
def cache_it(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = repr(*args, **kwargs)
        try:
            result = CACHE[key]
        except KeyError:
            result = func(*args, **kwargs)
            CACHE[key] = result
        print('---*args---', args,
              '\n---**kwargs---', kwargs,
              '\n---key---', key,
              '\n---result---', result)
        return result
    return inner

# 正常的业务逻辑
@cache_it
def query(sql):
    time.sleep(2)
    result = 'execute %s' % sql
    return result


if __name__ == '__main__':
    start = time.time()
    query('select * from blog_post')
    print(time.time() - start)

    start = time.time()
    query('select * from blog_post')
    print(time.time() - start)