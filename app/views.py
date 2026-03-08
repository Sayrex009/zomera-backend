from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import *
from .serializers import *
from .utils import send_otp_email, generate_otp
from app.services.otp import generate_otp, send_otp_email, save_otp, verify_otp
from listing.models import *
from django.db.models import Q
User = get_user_model()

class RegisterEmailAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email va parol talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Bu email allaqachon ro'yxatdan o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_otp()
        save_otp(email, otp_code)
        send_otp_email(email, otp_code)

        request.session["register_password"] = password
        request.session["register_email"] = email

        return Response({"message": "OTP kod emailingizga yuborildi"}, status=status.HTTP_200_OK)


class VerifyEmailOTPAPI(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        email = request.session.get("register_email")
        password = request.session.get("register_password")

        if not email or not password:
            return Response({"error": "Sessiya topilmadi. Avval ro'yxatdan o'ting"}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_otp(email, otp):
            return Response({"error": "Noto'g'ri yoki muddati o'tgan OTP kod"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        request.session.flush()

        return Response({"message": "Ro'yxatdan o'tish muvaffaqiyatli", "user_id": user.id}, status=status.HTTP_201_CREATED)

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

class AdvertisementListAPI(APIView):
    def get(self, request):
        ads = Advertisement.objects.all()
        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)
    
class AnnouncementListAPI(APIView):
     def get(self, request, pk):
        try:
            ad = announcement.objects.get(id=pk)
        except announcement.DoesNotExist:
            return Response({"error": "Объявление не найдено"}, status=status.HTTP_404_NOT_FOUND)

        ad.views += 1
        ad.save()

        serializer = AdvertisementSerializer(ad)
        return Response(serializer.data)
     
class FavoriteListAPI(APIView):
       def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        try:
            product = announcement.objects.get(id=product_id)
        except announcement.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=user, product=product)
        if not created:
            favorite.delete()
            return Response({"message": "Sevimlilardan o'chirildi"}, status=status.HTTP_200_OK)
        return Response({"message": "Sevimlilarga qo'shildi"}, status=status.HTTP_201_CREATED)
       
class SearchAnnouncementAPI(APIView):
    def get(self, request):
        query = request.GET.get("q", "") 

        if query:
            ads = announcement.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(address__icontains=query)
            )
        else:
            ads = announcement.objects.all()

        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)