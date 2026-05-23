import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Food, Reservation, Restaurant, User


class FoodSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Food
        fields = [
            'id', 'restaurant', 'restaurant_name', 'name', 
            'description', 'price', 'image', 'is_available', 
            'food_type', 'is_booked'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Taom narxi 0 dan katta bo'lishi shart!")
        return value



class ReservationSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')
    
    class Meta:
        model = Reservation
        fields = ['id', 'food', 'food_name', 'status', 'reserved_at']
        read_only_fields = ['status']



class RestaurantSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'owner_email', 'name', 'address', 'phone']
        read_only_fields = ['owner']

    def validate_phone(self, value):
        
        phone_regex = r'^\+998\d{9}$'
        if value and not re.match(phone_regex, value):
            raise serializers.ValidationError("Telefon raqami '+998XXXXXXXXX' formatida bo'lishi shart!")
        return value



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'password']
        extra_kwargs = {
            # Parol ro'yxatdan o'tishda majburiy bo'lishi kerak!
            'password': {'write_only': True, 'required': True},
            'email': {'validators': []},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True}
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email maydoni bo'sh bo'lishi mumkin emas!")
        
        user_id = self.instance.id if self.instance else None
        email_count = User.objects.filter(email=value).exclude(id=user_id).count()
        
        if email_count >= 3:
            raise serializers.ValidationError("Bu email manziliga maksimal 3 ta akkaunt biriktirilishi mumkin!")
        
        return value

    def validate_username(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(username=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Ushbu username band! Boshqa nom kiriting.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'client'),
            password=password
        )
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['token'] = data['access'] 
        return data