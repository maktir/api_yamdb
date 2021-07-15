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
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass
