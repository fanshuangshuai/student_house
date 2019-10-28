# coding=utf-8
import time

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class TimeItMiddleware(MiddlewareMixin):
    '''process_request() :是request来到middleware时进入的第一个方法
        :return HttpResponse 接下来的处理方法只会执行process_response
        :return None '接下来会执行其他方法
    '''
    def process_request(self, request):
        self.start_time = time.time()
        return

    '''在process_request()之后执行，参数func是view()
       process_view() 只在 Django 调用视图前被调用。
    '''
    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('student:index'):
            return None

        start = time.time()
        response = func(request)
        consted = time.time() - start
        print('process view : {:.2f}s'.format(consted))
        return response

    '''发生异常时，进入这个方法'''
    def process_exception(self, request, exception):
        pass

    '''执行完view()之后，拿到response，如果使用了template的response就会进入这个方法，对response进行操作'''
    def process_teamplate_response(self, request, response):
        return response

    '''如果使用了不带template的response就会进入这个方法，对response进行操作'''
    def process_response(self, request, response):
        costed = time.time() - self.start_time
        print('request to response cose: {:.2f}s'.format(costed))
        return response


class TimeItMiddleware2:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('暂停开始')
        time.sleep(5)
        print('暂停结束')
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response