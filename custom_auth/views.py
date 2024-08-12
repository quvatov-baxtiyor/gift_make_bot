import django_filters
from rest_framework import status, viewsets
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    RegisterSerializer, ProfileSerializer, CustomUserSerializer
)
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, LogoutSerializer, AccessRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView

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


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name'),
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={
            205: openapi.Response(
                description="Successfully logged out",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Success status'),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Blacklisted token'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Error status'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)

            # Blacklist the token
            token.blacklist()

            # Log out the user
            logout(request)

            data = {
                "status": True,
                "token": str(token),
                "message": "Successfully logged out"
            }
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            data = {
                'status': False,
                'message': 'Token error: {}'.format(str(e))
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                'status': False,
                'message': 'You are not logged in or an error occurred'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AccessRefreshView(TokenRefreshView):
    serializer_class = AccessRefreshSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                }
            ),
            400: openapi.Response(
                description="Invalid token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                description="Bearer Token", type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: ProfileSerializer,
            401: "Unauthorized"
        }
    )
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'country']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
    ordering_fields = ['full_name', 'country']
    ordering = ['-reg_date']
