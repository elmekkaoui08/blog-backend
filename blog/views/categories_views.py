from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from . import DefaultPagination
from ..models import Category
from ..serializers import CategorySerializer


class CategoriesList(ListAPIView):
    #permission_classes = (IsAuthenticated, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination


class  CategoriesCreate(CreateAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer


class CategoriesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'category_id'

