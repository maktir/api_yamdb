from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import (IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import SlidingToken
from users.models import User

from .models import Review, Title, Genre, Category
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    EmailCodeSendSerializer,
    UserSerializer,
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer
)


class ListCreateMixin(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    pass


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    pass


class RetrieveUpdateDeleteViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    pass


@api_view(['POST'])
def email_token_obtain_view(request):
    user = get_object_or_404(User, email=request.data['email'])
    if request.data['confirmation_code'] == user.password:
        token = str(SlidingToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


class EmailCodeSendView(APIView):

    def post(self, request):
        serializer = EmailCodeSendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, email=request.data['email'])
            send_mail('Confirmation', user.password, 'from@emperor.com', [user.email])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly | IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.all()
        return User.objects.filter(username=self.kwargs.get('username'))

    @action(detail=False, methods=['get', 'patch'],
            url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly|IsAuthorOrReadOnly|
                          IsAdminUser]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if self.action == 'list':
            return title.reviews.all()
        else:
            return title.reviews.filter(pk=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly|IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        if self.action == 'list':
            return review.comments.all()
        else:
            return review.comments.filter(pk=self.kwargs.get('comment_id'))

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'genre', 'year', 'name']

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
