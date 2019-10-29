from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from config.models import Link, SiderBar
from student_sys.custom_site import custom_site


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'created_time', 'owner', 'operator']

    # admin页面（操作页面）要显示的字段
    fields = (
        'title',
        'href',
        'status',
        'weight',
    )

    # 过滤器，允许人们以 category 字段来过滤列表
    list_filter = ['title', 'href']

    # 搜索框，搜索 …… 字段
    search_fields = ['title', 'href']


    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:config_link_change', args=(obj.id, ))
        )
    # 指定表头的展示文案
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SiderBar, site=custom_site)
class SiderBarAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_type', 'content', 'created_time']
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)
