from dataclasses import fields
from rest_framework import serializers
from .models import User, FriendRequest
 
class RegistrationSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = User
        fields = ['name', 'password',
                  'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):

        password = self.validated_data['password']
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'email already exist'})

        account = User(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
        )
        account.password = password
        account.save()
        return account

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', ]


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = '__all__'