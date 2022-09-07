from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from ..models import Article, User, Comment
from ..serializers import CommentSerializer


class CommentCreate(CreateAPIView):
    serializer_class = CommentSerializer
    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data.get('user_id'))
        article = Article.objects.get(pk=request.data.get('article_id'))
        comment = Comment()
        comment.user = user
        comment.article = article
        comment.content = request.data.get('comment')
        comment.save()
        serializer = CommentSerializer(data=comment)
        serializer.is_valid()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
