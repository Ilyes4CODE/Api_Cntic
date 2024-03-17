from rest_framework import serializers
from .models import Post,Comment,Profile,Event


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','content','created_time','comments','author','image','likers','dislikers','edited')
        extra_kwargs = {
            'content' : {'required': True },
            'created_time' : {'required': False },
            'comments' : {'required': False },
            'author' :{'required': False },
            'image' : {'required': False},
            'dislikers' : {'required': False },
            'likers' : {'required': False},
            'edited' : {'required': False},
        }



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        #fields = ('id','author','content','parent_post','created_time','likers','dislikers')
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','user','name','picture','email','phone','is_banned','univ_id')
        extra_kwargs = {
            'name' : {'required': True },
            'user' : {'required': True },
            'picture' : {'required': False },
            'email' :{'required': True },
            'phone' : {'required': False},
        }


class UpadteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'picture', 'email', 'phone', 'univ_id']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'Title', 'Description', 'image', 'count', 'enrolled_users']