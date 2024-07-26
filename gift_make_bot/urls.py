from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from custom_auth.views import RegisterView, CustomTokenObtainPairView, LogoutView, ProfileUserView

schema_view = get_schema_view(
    openapi.Info(
        title="Gift Make Bot API",
        default_version='v1',
        description="API documentation for Gift Make Bot",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@giftmakebot.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('custom_auth.urls')),  # Include your custom_auth URLs
                  path('api/', include('body.urls')),  # Include your body app URLs
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
