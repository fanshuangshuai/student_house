# coding=utf-8
from rest_framework import serializers, pagination

from .models import Post, Category


# class PostSerializer(serializers.ModelSerializer):
class PostSerializer(serializers.HyperlinkedModelSerializer):
    """类似于Django的Form，提供了类似forms.Form和forms.ModelForm的类（serializers.Serializer和serializers.ModelSerializer）
    以下是文章列表接口需要的Serializer；
    SlugRelatedField的用法：
        如果是FK外键的话，需要配置SlugRelatedField，定义FK是否可写（read_only参数）；
        如果是多对多的话，需要配置many=True；
        slug_field参数指定要展示的字段是什么。
    """
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

    class Meta:
        model = Post
        # id用来获取详情接口的数据，其他字段用来展示概要信息，且不用返回正文。
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'created_time']


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        # 详情页还需要提供content字段的输出。
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time',
        )


class CategoryDetailSerializer(CategorySerializer):
    # 把posts字段获取的内容映射到 paginated_posts()
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializers = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializers.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'posts'
        )
