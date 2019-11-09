from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from blog.models import Tag, Post, Category
from comment.forms import CommentForm
from comment.models import Comment
from config.models import SiderBar, Link
from student_sys.common import time_it


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        """获取上下文数据并最终将其传入模板"""
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SiderBar.get_all()
        })
        context.update(Category.get_navs())
        # print('======CommonViewMixin.get_context_date():', context, '======')
        return context


class IndexView(CommonViewMixin, ListView):
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
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     host_posts = Post.hot_posts()
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'host_posts': host_posts,
#         'sidebars': SiderBar.get_all(),
#     }
#     context.update(Category.get_navs())     # 此时，context的属性包括：category/tag/post_list/host_posts/sidebars/navs/categories
#
#     return render(request, 'blog/list.html', context=context)


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

    # def get_context_data(self, **kwargs):
    #     """重写get_context_data，为了通过View层把CommentForm和评论的数据传递到模板层"""
    #     context = super().get_context_data(**kwargs)
    #     post_id = self.kwargs.get('post_id')
    #     post = Post.objects.get(id=post_id)
    #     context.update({
    #         # 'comment_form': CommentForm,
    #         # 'comment_list': Comment.get_by_target(self.request.path),
    #         'post': post,
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # 这样实现文章访问统计，性能太低（过多执行写操作）
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)

        # 调试用
        # from django.db import connection
        # print(connection.queries)
        # return response

        self.hand_visited()
        return response

    def hand_visited(self):
        """
        判断是否有缓存，如果没有则进行 +1 操作，并且避免执行两次更新操作
        :return:
        """
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        print('======PostDetailView.hand_visited.pv_key :', pv_key, ' \nuv_key :', uv_key, '======')
        print(cache)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)      # 1 分钟有效

        if not cache.get(uv_key):
            increase_pv = True
            cache.set(pv_key, 1, 24*60*60)  # 24 小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    """
    后台先执行get_queryset()，再执行get_context_data()
    """
    def get_context_data(self):
        print('======run SearchView get_context_date()======')
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        print('======run SearchView get_queryset()======')
        # queryset查询到所有的记录
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # Q: select * from post where title ilike '%<keyword>%' or title ilike '%<keyword>%'
        # queryset.filter查询到过滤的记录
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        # exp: target='/post/12.html'
        target = request.POST.get('target')

        if comment_form.is_valid():

            # 此处以后补充功能：不实时展示评论，需要网管审核通过后才能展示

            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)