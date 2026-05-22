from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .models import User
from drf_spectacular.utils import extend_schema

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user_to_delete = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)
            
        if request.user.is_superuser or request.user.id == user_to_delete.id:
            user_to_delete.delete()
            return Response({"detail": "Akkaunt muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"detail": "Sizda ushbu akkauntni o'chirish huquqi yo'q!"}, 
            status=status.HTTP_403_FORBIDDEN
        )

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def patch(self, request, pk, *args, **kwargs):
        try:
            user_to_update = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_superuser or request.user.id == user_to_update.id:
            serializer = UserSerializer(user_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(
            {"detail": "Sizda ushbu profil ma'lumotlarini tahrirlash huquqi yo'q!"}, 
            status=status.HTTP_403_FORBIDDEN
        )

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

@extend_schema(responses=CustomTokenObtainPairSerializer)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer