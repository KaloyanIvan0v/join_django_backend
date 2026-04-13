from rest_framework import viewsets
from app_user_auth.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, EmailAuthTokenSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            refresh = RefreshToken.for_user(saved_account)
            data = {
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': saved_account.username,
                'display_name': getattr(saved_account.profile, 'display_name', ''),
                'email': saved_account.email,
            }
        else:
            data = serializer.errors
        return Response(data)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'display_name': getattr(user.profile, 'display_name', ''),
                'email': user.email,
            }
        else:
            data = serializer.errors
        return Response(data)
