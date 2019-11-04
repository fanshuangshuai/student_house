# coding=utf-8
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms

from blog.models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    """
    django-autocomplete-light提供Form层的组件来加入后端接口
    """
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
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


    # 为了避免出现JS资源冲突的问题，定义了Meta以及其中的fields，需要把自动补全的字段放到前面
    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')