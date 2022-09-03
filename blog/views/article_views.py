from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ..models import Article, Post, Author
from ..serializers import ArticleSerializer, PostSerializer


class DefaultPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000

class ArticleList(ListAPIView):
    #permission_classes = (IsAuthenticated, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'content')

    #get articles by category
    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category is None:
            return super().get_queryset()
        queryset = Article.objects.filter(category_id=category)
        return queryset

class ArticleCreate(CreateAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = ArticleSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # TODO: must change to get the connected user as the author for the post
        article = Article.objects.get(pk=response.data.get('article_id'))
        author = Author.objects.get(pk=1)
        author.nbr_of_posts += 1
        author.save()
        post = Post(author=author, article=article)
        post.save()
        serializer = PostSerializer(data=post)
        serializer.is_valid()
        print('Serializer: ', serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ArticleRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'article_id'

    def delete(self, request, *args, **kwargs):
        article = self.get_object()
        posts = Post.objects.filter(article_id=article.article_id)
        for post in posts:
            post.author.nbr_of_posts -= 1
            post.author.save()
        return super().delete(request, *args, **kwargs)
