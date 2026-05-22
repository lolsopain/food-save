from django.urls import path
from .views import RegisterView, UserViewSet, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('<int:pk>/', UserViewSet.as_view(), name='user-detail'),
]