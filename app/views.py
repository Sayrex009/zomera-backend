from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, PhoneOTP
from .utils import send_sms, generate_otp

class RegisterAPI(APIView):
    def post(self, request):
        phone = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone or not password:
            return Response({"error": "Telefon raqami va parol kerak"}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_otp()

        PhoneOTP.objects.update_or_create(
            phone_number=phone,
            defaults={"otp": otp_code, "is_verified": False}
        )

        send_sms(phone, f"Sizning tasdiqlash kodingiz: {otp_code}")

        request.session["phone_number"] = phone
        request.session["password"] = password

        return Response({"message": "OTP kodingiz yuborildi"}, status=status.HTTP_200_OK)


class VerifyOTPAPI(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        phone = request.session.get("phone_number")
        password = request.session.get("password")

        if not phone or not password:
            return Response({"error": "Seshiyadagi ma'lumotlar topilmadi"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            phone_otp = PhoneOTP.objects.get(phone_number=phone)
            if phone_otp.otp == otp and not phone_otp.is_expired():
                user = User.objects.create_user(phone_number=phone, password=password)
                phone_otp.is_verified = True
                phone_otp.save()
                return Response({"message": "Ro'yxatdan o'tish muvaffaqiyatli"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Noto'g'ri OTP yoki OTP muddati tugagan"}, status=status.HTTP_400_BAD_REQUEST)
        except PhoneOTP.DoesNotExist:
            return Response({"error": "OTP kod topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
