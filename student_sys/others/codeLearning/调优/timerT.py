# coding=utf-8
import time
import requests


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, 'cost', time.time() - start)
        return result
    return wrapper


@time_it
def fetch_page(url):
    requests.get(url)

url = 'http://www.sohu.com'
fetch_page(url)