from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from ..models import Article, User, Comment
from ..serializers import CommentSerializer


class CommentCreate(CreateAPIView):
    serializer_class = CommentSerializer
    # def create(self, request, *args, **kwargs):
    #     article = Article.objects.get(pk=request.data.get('article_id'))
    #     comment = Comment()
    #     comment.article = article
    #     comment.content = request.data.get('comment')
    #     comment.save()
    #     serializer = CommentSerializer(data=comment)
    #     serializer.is_valid()
    #     return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class CommentList(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset