from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, foods_page

router = DefaultRouter()
router.register(r'', FoodViewSet)

urlpatterns = [
    path('page/', foods_page, name='foods-page'),
    path('', include(router.urls)),
]