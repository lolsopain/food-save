from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'food',
            'food_name',
            'status',
            'reserved_at'
        ]
        # Oddiy foydalanuvchi yangi buyurtma ochayotganda statusni o'zi 'completed' qilib yuborolmaydi
        read_only_fields = ['status']