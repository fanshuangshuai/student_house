# coding=utf-8
from .base import *     # NOQA

DEBUG = False

ALLOWED_HOSTS = ['daemonnnn.xyz']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_sys_product_db',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'POST': 3306,
        # 配置持久化连接
        'CONN_MAX_AGE': 5 * 60,
        # 配置mysqlclient连接
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}