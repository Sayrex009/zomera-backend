from django.contrib import admin
from django.urls import path
from app.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/register/", RegisterEmailAPI.as_view()),
    path("api/verify/", VerifyEmailOTPAPI.as_view()),
    path("api/login/", LoginAPI.as_view()),
    path('admin/', admin.site.urls),
    path('api/announcements/<int:pk>/', AnnouncementListAPI.as_view(), name='announcement-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/ads/', AdvertisementListAPI.as_view(), name='advertisement-list'),
    path('api/search/', SearchAnnouncementAPI.as_view(), name='search-announcements'),
    path('api/favorites/', FavoriteListAPI.as_view(), name='favorite-list'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

