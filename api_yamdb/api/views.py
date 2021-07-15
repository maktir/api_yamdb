from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_mail("here's your JWT. Enjoy!", serializer.validated_data,
                  'from@example.com', ['to@example.com'])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)