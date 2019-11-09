# coding=utf-8
from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """配置所欲需要自动补全的接口（自动补全的View层）"""
    def get_queryset(self):
        # is_authenticated 检查用户是否登录
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        # 获取该用户创建的所有分类
        qs = Category.objects.filter(owner=self.request.user)
        # q : 是url参数传递过来的值，
        # 比如http://127.0.0.1:8000/category-autocomplete/?q=dj
        # 那么self.q = dj
        print('------Category : self.q :', self.q, '------')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        print('------Category : qs :', qs, '------')
        return qs

class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()
        # 获取该用户创建的所有标签
        qs = Tag.objects.filter(owner=self.request.user)
        # q : 是url参数传递过来的值
        print('------Tag : self.q :', self.q, '------')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        print('------Tag : qs :', qs, '------')
        return qs

