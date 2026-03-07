from django.contrib import admin
from django.urls import path
from app.views import RegisterEmailAPI, VerifyEmailOTPAPI

urlpatterns = [
    path('register-email/', RegisterEmailAPI.as_view(), name='register-email'),
    path('verify-email-otp/', VerifyEmailOTPAPI.as_view(), name='verify-email-otp'),
]

