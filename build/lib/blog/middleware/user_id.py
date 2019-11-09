# coding=utf-8
import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 生成uid
        uid = self.generate_uid(request)
        # 动态给request添加uid属性
        request.uid = uid
        response = self.get_response(request)
        # 返回response时，我们设置cookie
        # httponly：只能在服务端能访问
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid