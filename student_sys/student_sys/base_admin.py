# coding=utf-8
from django.contrib import admin

class BaseOwnerAdmin(object):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    # def get_queryset(self, request):
    #     """
    #     admin写法
    #     让当前登录的用户在列表页中只能看到自己创建的文章"""
    #     qs = super(BaseOwnerAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # def save_model(self, request, obj, form, change):
    #     """重写save_model()的作用是：保存数据前，把owner字段的值设置为当前登录用户，将数据写入数据库"""
    #     obj.owner = request.user
    #     return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_list_queryset(self):
        """
        xadmin写法
        xadmin中需要参数传递的数据都可以通过self对象获取到
        让当前登录的用户在列表页中只能看到自己创建的文章
        """
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        """重写save_model()的作用是：保存数据前，把owner字段的值设置为当前登录用户，将数据写入数据库"""
        self.new_obj.owner = self.request.user
        return super().save_models()