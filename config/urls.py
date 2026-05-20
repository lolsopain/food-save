from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Bu yerga login_page ham qo'shildi (agar views.py ichida yozgan bo'lsangiz)
from config.views import home, foods_page 
from django.views.generic import TemplateView # <-- Agar view yozishni xohlamasangiz, tayyor shablon ochuvchi

urlpatterns = [
    # Sahifalar (Frontend HTML)
    path('', home, name='home'),
    path('foods-page/', foods_page, name='foods-page'),
    
    # 📌 LOGIN SAHIFASI UCHUN YANGI YO'LAK (404 xatosini yo'qotadi)
    path('login-page/', TemplateView.as_view(template_name='login.html'), name='login-page'),

    # Admin panel
    path('admin/', admin.site.urls),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # AUTH
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps (API endpoints)
    path('api/restaurants/', include('restaurants.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/reservations/', include('reservations.urls')),
]