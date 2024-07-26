from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from body.models import UserChat, ChatInitCategory, ChatCategory
from body.serializers import UserChatSerializer, ChatInitCategorySerializer, ChatCategorySerializer


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChatInitCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatInitCategory.objects.all()
    serializer_class = ChatInitCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class ChatCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatCategory.objects.all()
    serializer_class = ChatCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
