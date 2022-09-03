from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import User
from ..serializers import UserSerializer


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

