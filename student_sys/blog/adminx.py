import xadmin
from crispy_forms.layout import Fieldset, Row
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Container

from blog.adminforms import PostAdminForm
from student_sys.base_admin import BaseOwnerAdmin
from student_sys.custom_site import custom_site
from .models import Category, Tag, Post


# admin写法
# class PostInline(admin.TabularInline):      # StackedInline样式不同
class PostInline:
    # admin写法 fields = ('title', 'desc')
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1   # 控制额外多几个
    model = Post


# @admin.register(Category, site=custom_site)
@xadmin.sites.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
class CategoryAdmin(BaseOwnerAdmin):

    # 在同一页面编辑关联数据
    inlines = [PostInline, ]

    # 列表页面展示的列标题排序
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # admin页面（操作页面）要显示的字段
    fields = ('name', 'status', 'is_nav')

    # 搜索框，搜索 …… 字段
    search_fields = ['name']

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


# @admin.register(Tag, site=custom_site)
@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')

class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        """
        test()确认字段是否需要被当前的过滤器处理。
        """
        return field.name == 'category'

    def __init(self, field, request, params, model, model_admin, field_path):
        # 首先执行父类的__init__()
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新d定义self.lookup_choices的值，这个值在默认情况下（也就是在父类中）查询所有的数据。根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).value_list('id', 'name')
        # 把定义的过滤器注册到过滤器管理器中，并且设置优先权，这样才会在页面加载时使用我们定义的这个过滤器
        manager.register(CategoryOwnerFilter, take_priority=True)


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     """自定义过滤器只显示当前用户的分类"""
#
#     title = '分类过滤器'
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
#         return Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#     def queryset(self, request, queryset):
#         category_id =self.value()
#         if category_id:
#             return queryset.filter(category_id=self.value())
#         return queryset


# 简单实现一下has_add_permission
PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"

# @admin.register(Post)
# @admin.register(Post, site=custom_site)
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    # 不显示的字段
    exclude = ('owner', )

    # 在列表页面展示的字段，可设置自定义字段"operator"
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    # 列表页面可作为链接点击的列标题
    list_display_links = []

    # 过滤器，允许人们以 category 字段来过滤列表
    # list_filter = ['category', ]
    # list_filter = [CategoryOwnerFilter, ]
    list_filter = ['category', ]      # 注意这里不是定义的filter类，而是字段名

    # 搜索框，搜索 …… 字段
    search_fields = ['title', 'category__name']

    # 动作的相关配置，是否展示在顶部
    actions_on_top = True
    # 动作的相关配置，是否展示在底部
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # # admin页面（操作页面）要显示的字段
    """
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )    
    """

    # fieldsets控制布局
    # (名称, {内容}),
    # (名称, {内容}),
    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ('title', 'category'),
    #             'status',
    #         ),
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         ),
    #     }),
    #     ('额外信息', {
    #         # 'classes': ('collapse', ),
    #         'classes': ('wide', ),
    #         'fields': ('tag', ),
    #     })
    # )

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    # 横向展示OR纵向展示
    # filter_horizontal = ('tag', )
    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id, ))
            # reverse('cus_admin:blog_post_change', args=(obj.id, ))
            reverse('xadmin:blog_post_change', args=(obj.id, ))
        )
    # 指定表头的展示文案
    operator.short_description = '操作'

    # 自定义静态资源引入,下面的写法兼容admin、xadmin
    # @property
    # def media(self):
        # xadmin 基于Bootstrap，引入会导致页面样式冲突，这里只做演示
        # media = super().media
        # media.add_js(['https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js'])
        # media.add_css({
        #     'all': ("https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css", ),
        # })
        # return media

    # class Media:
    #     css = {
    #         'all': ("https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css", ),
    #     }
    #     js = ('"https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js', )


# xadmin自带了log功能，并且会默认配置好展示逻辑，所以注释掉admin-log配置
# @admin.register(LogEntry, site=custom_site)
# @xadmin.sites.register
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user',
#                     'change_message']