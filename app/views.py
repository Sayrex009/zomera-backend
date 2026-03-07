from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .utils import send_otp_email, generate_otp

User = get_user_model()

class RegisterEmailAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email va parol talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_otp()

        # Сохраняем в сессию для проверки
        request.session["email"] = email
        request.session["password"] = password
        request.session["otp"] = otp_code

        send_otp_email(email, otp_code)

        return Response({"message": "OTP kod yuborildi"}, status=status.HTTP_200_OK)


class VerifyEmailOTPAPI(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        email = request.session.get("email")
        password = request.session.get("password")
        otp_session = request.session.get("otp")

        if not email or not password or not otp_session:
            return Response({"error": "Sessiya topilmadi. Birinchi bo'lib ro'yxatdan o'ting"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_session == otp:
            User.objects.create_user(email=email, password=password)
            request.session.flush()
            return Response({"message": "Muofaqatli ro'yxatdan o'tdi"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Noto'ri OTP kod"}, status=status.HTTP_400_BAD_REQUEST)
