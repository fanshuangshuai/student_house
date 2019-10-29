from .base import *  # NOQA

# 开发环境中，DEBUG=True是可以的；线上环境不行！
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_sys',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '1234',
        # 'TEST': {
        #     'NAME': 'test_student_sys_db'
        # }
    }
}