from rest_framework import serializers
from base.models import Post
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class SignUpSerializer(serializers.ModelSerializer):
    univ_id = serializers.IntegerField(required=True)
    phone = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'univ_id', 'phone')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'password','username')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user is None:
            raise AuthenticationFailed("Incorrect username or password")

        # Assuming your user model has 'first_name' and 'last_name' fields
        refresh = self.get_token(user)               
        data['user'] = {
            'id': user.id,
            'first_name': user.first_name,  # Corrected field name to 'first_name'
            'last_name': user.last_name,    # Corrected field name to 'last_name'
            'username': user.username,
            'email': user.email,
            'groups': list(user.groups.values_list('name', flat=True)),  # Extract user groups
        }
        data['status'] = True
        return data