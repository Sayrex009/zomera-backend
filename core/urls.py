from django.contrib import admin
from django.urls import path
from app.views import RegisterAPI, VerifyOTPAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterAPI.as_view(), name='api_register'),
    path('api/verify-otp/', VerifyOTPAPI.as_view(), name='api_verify_otp'),

]
