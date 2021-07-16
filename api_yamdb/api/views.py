from .models import Title, Genre, Category
from rest_framework import viewsets, filters, mixins
from .serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer
)
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly


class ListCreateMixin(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'genre', 'year', 'name']

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save()
