from datetime import timedelta

import django_filters
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, CustomUserSerializer
)
from .models import CustomUser

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: CustomUserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):  # Inherit from SimpleJWT's view
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=CustomTokenObtainPairSerializer,
        manual_parameters=[
            openapi.Parameter(
                'fields',
                openapi.IN_QUERY,
                description="Comma-separated list of fields to include in user_data (e.g., 'full_name,email'). If not provided, all fields will be included.",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),

                    'user_data': openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True),
                },
            ),
            401: openapi.Response(description="Invalid credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token for logout')
            }
        ),
        responses={
            205: openapi.Response(description="Reset Content"),
            400: openapi.Response(description="Bad Request"),
            401: openapi.Response(description="Unauthorized"),
        }
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                description="Bearer Token", type=openapi.TYPE_STRING
            )
        ],
        responses={200: ProfileSerializer}
    )
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'country']  # Filter fields here


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')  # Ensure ordering
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
    ordering_fields = ['full_name', 'country']
    ordering = ['-reg_date']  # Default ordering by request date in descending order
