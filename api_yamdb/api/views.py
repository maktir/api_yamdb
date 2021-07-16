
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins, permissions
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from .models import Comment, Review, Title, Genre, Category
from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer, GenreSerializer, CategorySerializer


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in SAFE_METHODS)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def partial_update(self, request, pk):
        pass

    def destroy(self, request, pk):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if title.review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            title.review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def partial_update(self, request, pk):
        pass

    def destroy(self, request, pk):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        if review.comments.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            review.comments.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
