from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from app.models import EmailOTP
from .serializers import AdvertisementSerializer 
from app.services.otp import generate_otp, send_otp_email, save_otp, verify_otp
from listing.models import announcement, Favorite, Category

User = get_user_model()


class RegisterEmailAPI(APIView):
    """
    Шаг 1: Принимаем Email и Пароль, отправляем OTP.
    Данные сохраняются во фронтенде (React), а не в сессии.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email va parol talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Bu email allaqachon ro'yxatdan o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_otp()
        save_otp(email, otp_code)
        
        try:
            send_otp_email(email, otp_code)
            return Response({"message": "OTP kod emailingizga yuborildi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Email yuborishda xatolik: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmailOTPAPI(APIView):
    """
    Шаг 2: Проверяем OTP и создаем пользователя.
    Ожидает: email, password, code (otp).
    """
    def post(self, request):
        otp = request.data.get("code")
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not otp or not password:
            return Response({"error": "Ma'lumotlar to'liq emas (email, parol va kod kerak)"}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_otp(email, otp):
            return Response({"error": "Noto'g'ri yoki muddati o'tgan OTP kod"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if User.objects.filter(email=email).exists():
                return Response({"error": "Foydalanuvchi allaqachon yaratilgan"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(email=email, password=password)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Xatolik yuz berdi: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email va parol talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Email yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })



class AdvertisementListAPI(APIView):
    def get(self, request):
        
        ads = announcement.objects.all().order_by('-id')
        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)
    

class AnnouncementListAPI(APIView):
    def get(self, request, pk):
        try:
            ad = announcement.objects.get(id=pk)
            ad.views += 1
            ad.save()
            serializer = AdvertisementSerializer(ad)
            return Response(serializer.data)
        except announcement.DoesNotExist:
            return Response({"error": "E'lon topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class FavoriteListAPI(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Avval tizimga kiring"}, status=status.HTTP_401_UNAUTHORIZED)
            
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
            ).distinct()
        else:
            ads = announcement.objects.all()

        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)    