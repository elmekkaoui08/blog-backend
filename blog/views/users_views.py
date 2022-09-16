from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from . import DefaultPagination
from ..models import User
from ..serializers import UserSerializer


class UsersList(ListAPIView):
    #permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        user_type = self.request.query_params.get('user_type')
        if user_type is not None:
            queryset = User.objects.filter(role_id=user_type)
            return queryset

        return super().get_queryset()

class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

