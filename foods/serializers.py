from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    # Restoran nomini frontendga oson chiqarish uchun siz yozgan ReadOnlyField saqlandi
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Food
        fields = [
            'id', 
            'restaurant', 
            'restaurant_name', 
            'name', 
            'description', 
            'price', 
            'image',            # Taom rasmi uchun
            'is_available',     # Mavjudlik holati
            'food_type',        # Yangi / Qolgan ovqat turi
            'is_booked'         # Band qilinganlik holati
        ]