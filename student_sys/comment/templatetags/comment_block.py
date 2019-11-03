# coding=utf-8
from django import template

from comment.forms import CommentForm
from comment.models import Comment

register =template.Library()

@register.inclusion_tag('comment/block.html')

def comment_block(target):
    return {
        # 因为是自定义标签，默认是没有request对象的。所以手动将target渲染到页面
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }