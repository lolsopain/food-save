from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Food
        fields = ['id', 'restaurant', 'restaurant_name', 'name', 'description', 'price', 'is_available']