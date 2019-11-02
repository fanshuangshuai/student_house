"""student_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

from blog.views import post_list, PostDetailView, post_detail, PostListView, IndexView, CategoryView, TagView
from config.views import links
from .custom_site import custom_site


urlpatterns = [
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),

    path('student/', include('student.urls')),

    # https://127.0.0.1:8000/
    # url(r'^$', post_list, name='index'),
    url(r'^$', IndexView.as_view(), name='index'),

    # https://127.0.0.1:8000/category/1/
    # url(r'^category/(?P<category_id>\d+)/$', post_list, name='category-list'),
    url('^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),

    # https://127.0.0.1:8000/tag/1/
    # url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),

    # https://127.0.0.1:8000/post/2.html
    # url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),

    # https://127.0.0.1:8000/links/
    url(r'^links/$', links, name='links'),

]
