# coding=utf-8
from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_queryset(self, request):
        """让当前登录的用户在列表页中只能看到自己创建的文章"""
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        """重写save_model()的作用是：保存数据前，把owner字段的值设置为当前登录用户，将数据写入数据库"""
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
