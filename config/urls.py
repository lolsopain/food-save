from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView
from config.views import home, foods_page 
from django.views.generic import TemplateView
from users.views import CustomTokenObtainPairView

urlpatterns = [
    # Sahifalar (Frontend HTML shablonlari)
    path('', home, name='home'),
    path('foods-page/', foods_page, name='foods-page'),
    
    # AUTH SAHIFALARI (HTML shablonlar uchun yo'laklar)
    path('login-page/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('register-page/', TemplateView.as_view(template_name='register.html'), name='register-page'),

    # Admin panel
    path('admin/', admin.site.urls),

    # API docs (Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # AUTH API endpoints
    path('api/users/', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps (API endpoints)
    path('api/restaurants/', include('restaurants.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/reservations/', include('reservations.urls')),
]