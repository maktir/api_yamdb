from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import SlidingToken
from .serializers import (
    EmailCodeSendSerializer,
    UserSerializer,
)
from .permissions import IsAdminOrReadOnly
from users.models import User


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    pass


class RetrieveUpdateDeleteViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
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
    permission_classes = [IsAdminOrReadOnly | IsAdminUser]
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
