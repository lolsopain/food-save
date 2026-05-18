from rest_framework import viewsets, permissions
from django.shortcuts import render
from .models import Food
from .serializers import FoodSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_permissions(self):
        # Faqat adminlar ovqat qo'shishi, o'zgartirishi va o'chirishi mumkin
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        # Istalgan odam menyuni ko'ra oladi
        return [permissions.AllowAny()]

def foods_page(request):
    return render(request, 'foods.html')