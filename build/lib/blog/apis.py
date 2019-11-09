# coding=utf-8
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from blog.models import Post, Category
from blog.serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


# 可读写接口
# class PostViewSet(viewsets.ModelViewSet):
# 只读接口
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]    # 写入时的权限校验

    def retrieve(self, request, *args, **kwargs):
        # """在retrieve()中重新设置了serializer_class的值，这样不同接口使用不同Serializer"""
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """通过获取URL上Query中的category参数，重写类似get_queryset()来实现过滤"""
        category_id =self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)