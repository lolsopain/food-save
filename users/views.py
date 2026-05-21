from rest_framework import generics, permissions, viewsets, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .models import User

# 1. Ro'yxatdan o'tish
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# 2. Akkaunt boshqaruvi (O'chirish va Ismni yangilash)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.is_superuser or request.user.id == user_to_delete.id:
            user_to_delete.delete()
            return Response({"detail": "Akkaunt muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"detail": "Sizda ushbu akkauntni o'chirish huquqi yo'q! Faqat akkaunt egasi yoki admin o'chira oladi."}, 
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        user_to_update = self.get_object()
        if request.user.is_superuser or request.user.id == user_to_update.id:
            return super().partial_update(request, *args, **kwargs)
            
        return Response(
            {"detail": "Sizda ushbu profil ma'lumotlarini tahrirlash huquqi yo'q!"}, 
            status=status.HTTP_403_FORBIDDEN
        )


# 3. Parolni xavfsiz o'zgartirish
class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"detail": "Eski va yangi parollar kiritilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"detail": "Eski parol noto'g'ri kiritildi!"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Parol muvaffaqiyatli o'zgartirildi!"}, status=status.HTTP_200_OK)


# 4. Kengaytirilgan Login (Token) API oynasi
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer