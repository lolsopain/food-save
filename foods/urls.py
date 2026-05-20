from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet

router = DefaultRouter()
router.register(r'', FoodViewSet, basename='food')

urlpatterns = [
    # Frontend sahifa bu yerdan olib tashlandi, chunki u config/urls.py ichida TemplateView orqali to'g'ri sozlangan
    path('', include(router.urls)),
]