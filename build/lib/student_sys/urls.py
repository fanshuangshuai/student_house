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
import xadmin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from DRF_quickstart.views import UserViewSet, GroupViewSet
from blog.apis import PostViewSet, CategoryViewSet
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import PostDetailView, post_detail, PostListView, IndexView, CategoryView, TagView, \
    SearchView, AuthorView, LinkListView, CommentView
from config.views import links
from student_sys.autocomplete import CategoryAutocomplete, TagAutocomplete
from .custom_site import custom_site

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
    # path('super_admin/', admin.site.urls),
    # path('admin/', custom_site.urls),

    path('admin/', xadmin.site.urls, name='xadmin'),

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
    url(r'^links/$', LinkListView.as_view(), name='links'),

    url(r'^search/$', SearchView.as_view(), name='search'),

    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),

    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    # url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    # 缓存sitemap接口
    url(r'sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap), {'sitemaps': {'posts': PostSitemap}}),

    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),

    # ckeditor_uploader.urls提供了两个接口：接收上传图片和浏览已上传图片
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # django-rest-framework
    url(r'^api/', include((router.urls, 'api'))),
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/docs/', include_docs_urls(title='student_sys apis')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns