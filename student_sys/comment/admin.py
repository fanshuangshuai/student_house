from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['target', 'nickname', 'content', 'email', 'created_time', 'operator']

    # admin页面（操作页面）要显示的字段
    fields = (
        ('content', 'nickname'),
        'email',
        'status',
        # 'target',
    )

    # 列表页面可作为链接点击的列标题
    list_display_links = []

    # 过滤器，允许人们以 category 字段来过滤列表
    list_filter = ['content', ]

    # 搜索框，搜索 …… 字段
    search_fields = ['target', 'nickname']

    # 动作的相关配置，是否展示在顶部
    # actions_on_top = True
    # 动作的相关配置，是否展示在底部
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:comment_comment_change', args=(obj.id, ))
        )
    # 指定表头的展示文案
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CommentAdmin, self).save_model(request, obj, form, change)