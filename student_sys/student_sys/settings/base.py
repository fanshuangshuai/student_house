"""
Django settings for student_sys project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR='E:\\projects\\GitProjects\\student_house\\student_sys'
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(*h5fvr$mt4$p^1pdcn5gbfuee_m=ofd1578(yhdn406vdu79n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'testserver',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'comment.apps.CommentConfig',
    'config.apps.ConfigConfig',

    'student.apps.StudentConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'blog.middleware.user_id.UserIDMiddleware',
    'student.middlewares.TimeItMiddleware',
    # 'student.middlewares.TimeItMiddleware2',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'student_sys.urls'

# 指定主题文件的整体目录，包括模板和静态资源
# THEME = 'default'
THEME = 'bootstrap'

# 配置部署后的静态资源路径（项目上线后才会用到）
# STATIC_ROOT = '/tmp/static'

# 配置页面上静态资源的起始路径，比如博客列表页面中的CSS资源拆分之后的地址就是/static/css/base.css
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'

# 指定静态资源所在的目录。我们访问以上CSS文件时会在这个目录下面查找。
# 指定主题中静态资源所在的目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'themes', THEME, 'static'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # django模板的查找目录
        'DIRS': [os.path.join(BASE_DIR, 'themes', THEME, 'templates')],
        # 如果在 'DIRS'查找目录中找不到模板，就在每个APP下面寻找
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'student_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES 转入delevop.py


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'   # 语言
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'     # 时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True         # 语言

USE_L10N = True         # 数据和时间格式

USE_TZ = True           # 启动时区

# django debug toolbar
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
DEBUG_TOOLBAR_CONFIG = {
    # 'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
    # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
    #'JQUERY_URL': '/static/jquery/2.1.4/jquery.min.js',
    'SHOW_COLLAPSED': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: False,
}

