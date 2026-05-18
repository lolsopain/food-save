from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'owner_email', 'name', 'address', 'phone']
        read_only_fields = ['owner']