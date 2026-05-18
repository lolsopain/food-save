from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'client')
        )

        user.set_password(password)  # 🔥 HASH PASSWORD
        user.save()
        return user