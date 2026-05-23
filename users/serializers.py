from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 'phone' bu yerdan olib tashlandi
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}, # Parolni majburiy qildik
            'email': {'validators': []},
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
        # create_user ichidan ham phone olib tashlandi
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            role=validated_data.get('role', 'client'),
            password=password
        )
        return user
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
        # Frontenddan phone kelmasa, bo'sh matn sifatida saqlaydi
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