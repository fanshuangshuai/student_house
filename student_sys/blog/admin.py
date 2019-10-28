from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 列表页面展示的列标题排序
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    # admin页面（操作页面）要显示的字段
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 在列表页面展示的字段，可设置自定义字段"operator"
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    # 列表页面可作为链接点击的列标题
    list_display_links = []

    # 过滤器，允许人们以 category 字段来过滤列表
    list_filter = ['category', ]

    # 搜索框，搜索 …… 字段
    search_fields = ['title', 'category__name']

    # 动作的相关配置，是否展示在顶部
    actions_on_top = True
    # 动作的相关配置，是否展示在底部
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    # admin页面（操作页面）要显示的字段
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
    # 指定表头的展示文案
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)