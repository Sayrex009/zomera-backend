from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import send_otp_email, generate_otp

User = get_user_model()


class RegisterEmailAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email va parol talab qilinadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Bu email allaqachon ro'yxatdan o'tgan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_code = str(generate_otp())

        request.session["register_email"] = email
        request.session["register_password"] = password
        request.session["register_otp"] = otp_code

        send_otp_email(email, otp_code)

        return Response(
            {"message": "OTP kod emailingizga yuborildi"},
            status=status.HTTP_200_OK
        )


class VerifyEmailOTPAPI(APIView):
    def post(self, request):
        otp = request.data.get("otp")

        email = request.session.get("register_email")
        password = request.session.get("register_password")
        otp_session = request.session.get("register_otp")

        if not email or not password or not otp_session:
            return Response(
                {"error": "Sessiya topilmadi. Avval ro'yxatdan o'ting"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp != otp_session:
            return Response(
                {"error": "Noto'g'ri OTP kod"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            email=email,
            password=password
        )

        request.session.flush()

        return Response(
            {
                "message": "Ro'yxatdan o'tish muvaffaqiyatli",
                "user_id": user.id
            },
            status=status.HTTP_201_CREATED
        )


class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email va parol talab qilinadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Email yoki parol noto'g'ri"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })