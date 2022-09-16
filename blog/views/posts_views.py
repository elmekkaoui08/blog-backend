from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from ..views import DefaultPagination


class PostsList(ListAPIView):
    #permission_classes = (IsAuthenticated, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        category_id = self.request.query_params.get('category_id')
        if author_id is not None:
            queryset = Post.objects.filter(author_id=author_id)
            return queryset

        if category_id is not None:
            queryset = Post.objects.filter(article__category__category_id=category_id)
            return queryset
        return super().get_queryset()

class PostRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'post_id'

class CreateComment(CreateAPIView):
    serializer_class = CommentSerializer


