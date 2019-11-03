# coding=utf-8
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Post

class ExtendedRSSFeed(Rss201rev2Feed):
    """
    自定义feed_type来实现输出正文部分
    """
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    """
    使用Django的RSS模块Feed来实现RSS输出
    """
    # feed_type可以被赋值为其他类型，可以定制的！
    # feed_type = Rss201rev2Feed
    feed_type = ExtendedRSSFeed
    title = "Student BLog System"
    link = "/rss/"
    description = "student_sys is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html