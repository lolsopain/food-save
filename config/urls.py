from django.contrib import admin
from django.urls import path, include
from config.views import home
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from config.views import home, foods_page

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    path('', home, name='home'),
    path('foods-page/', foods_page, name='foods-page'),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # AUTH
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps
    path('api/restaurants/', include('restaurants.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/reservations/', include('reservations.urls')),
]