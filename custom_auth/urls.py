from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, ProfileUserView, UserViewSet,AccessRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('refresh_token/', AccessRefreshView.as_view())
]
