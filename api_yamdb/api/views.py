from django.db.models import Avg
from .mixins import CreateDestroyListMixinSet
from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import TitleFilter


class CategoryViewSet(CreateDestroyListMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_fields = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    # queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    # permission_classes =
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
