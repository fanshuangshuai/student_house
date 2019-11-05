# coding=utf-8
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms
from django.forms import model_to_dict
from django.forms.models import apply_limit_choices_to_to_formfield
from django.forms.utils import ErrorList

from blog.models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    """
    django-autocomplete-light提供Form层的组件来加入后端接口
    """
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    # content_ck和content_md是为了在页面展示的
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    # content 用来接收最终的编辑内容
    content = forms.CharField(widget=forms.HiddenInput(), required=False)



# 为了避免出现JS资源冲突的问题，定义了Meta以及其中的fields，需要把自动补全的字段放到前面
    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'is_md', 'content', 'content_md', 'content_ck',
            'status'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        """
        对Form做初始化处理
        :param instance: 当前文章的实例
        :param initial: Form中各字段初始化的值
        :param kwargs:
        """
        print('====== adminforms PostAdminForm init ======\n'
              '====== adminforms PostAdminForm instance : ', instance)
        initial = initial or {}
        if instance:
            print('------ instance有值！！！------')
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content
        print('====== instance :', instance)
        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        """
        对用户提交的内容做处理，
        判断是否使用了Markdown语法，
        然后设置获取对应编辑器的值，并将其赋值给content
        """
        is_md = self.cleaned_data.get('is_md')
        print('====== adminforms PostAdminForm clean ======\n,'
              '====== adminforms PostAdminForm clean.is_md :', is_md)
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        print('====== adminforms PostAdminForm clean.content :', content)
        if not content:
            self.add_error(content_field_name, '必填项！')
            return

        self.cleaned_data['content'] = content
        # self.content = content
        print('====== adminforms PostAdminFOrm clean.cleaned_data[content] :', self.cleaned_data['content'])
        # print('====== self.content :', self.content)
        return super().clean()

    class Media:
        print('====== adminforms PostAdminForm Media ======')
        """通过JS文件来实现展示逻辑的控制"""
        js = ('js/post_editor.js', )
