from rest_framework import serializers
from base.models import Post
from django.contrib.auth.models import User


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