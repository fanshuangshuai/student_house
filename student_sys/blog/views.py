from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from blog.models import Tag, Post, Category
from config.models import SiderBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        """获取上下文数据并最终将其传入模板"""
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SiderBar.get_all()
        })
        context.update(Category.get_navs())
        return context

class IndexView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')      # self.kwargs中的数据是从URL定义中拿到的。
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


"""
render(request, template_name, context=None, content_type=None, status=None, using=None)
-request: 封装了HTTP请求的request对象
"""
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    host_posts = Post.hot_posts()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'host_posts': host_posts,
        'sidebars': SiderBar.get_all(),
    }
    context.update(Category.get_navs())     # 此时，context的属性包括：category/tag/post_list/host_posts/sidebars/navs/categories

    return render(request, 'blog/list.html', context=context)


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 2
    context_object_name = 'post_list'   # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'



def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SiderBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'