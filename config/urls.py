from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import home, foods_page 
from django.views.generic import TemplateView
from users.views import CustomTokenObtainPairView

urlpatterns = [
    
    path('', home, name='home'),
    path('foods-page/', foods_page, name='foods-page'),
    path('login-page/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('register-page/', TemplateView.as_view(template_name='register.html'), name='register-page'),

   
    path('admin/', admin.site.urls),

    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    
    path('api/users/', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   
    path('api/restaurants/', include('restaurants.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/reservations/', include('reservations.urls')),
]