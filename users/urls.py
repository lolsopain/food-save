from django.urls import path
from .views import RegisterView, UserViewSet, ChangePasswordView

# Router-dan butunlay voz kechamiz va har bir yo'lni qo'lda aniq yozamiz:
urlpatterns = [
    # 1. Ro'yxatdan o'tish: POST /api/users/register/
    path('register/', RegisterView.as_view(), name='register'),
    
    # 2. Parolni o'zgartirish: POST /api/users/change-password/
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # 3. Profilni yangilash (PATCH) va o'chirish (DELETE): /api/users/<id>/
    path('<int:pk>/', UserViewSet.as_view({
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-detail'),
]