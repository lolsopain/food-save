from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, foods_page

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend ko'rinishlari
    path('', home, name='home'),
    path('foods-page/', foods_page, name='foods-page'),

    # JWT login endpoints
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger hujjatlari (Kurs ishi talabi)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API marshrutlari
    path('api/users/', include('users.urls')),
    path('api/foods/', include('foods.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/reservations/', include('reservations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)