from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from .serializers import SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Post,Profile
from base.serializer import PostSerializer,ProfileSerializer
from django.contrib.auth.models import Group
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView


class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response({
                'status': False,
                'message': "Incorrect username or password"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Routes(request):
    Route = [
         'Get_Profiles/',
         '/token/',
         '/token/refresh/',
         'register/',
         'CurrentUser/',
         'Posts_User/',
    ]
    return Response(Route)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_all_Profiles(request):
    if request.method == 'GET':
        if not request.user.groups.filter(name='Admin').exists():
            return Response({"Info":"you are not allowed to access"},status=status.HTTP_400_BAD_REQUEST)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"Info":"This is not a GET request"},status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            profile = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password'])
            )
            Profile.objects.create(user=profile,email=data['email'],name=data['first_name'] + ' ' + data['last_name'],univ_id = data['univ_id'],phone = data['phone'])
            group = Group.objects.get(name="User")
            profile.groups.add(group)
            return Response({'Details':'Account Created Successfully'},status=status.HTTP_201_CREATED)
        else : 
            return Response({'Error':'Account Already Exists'},status=status.HTTP_400_BAD_REQUEST)
    else : 
        return Response(user.errors)
   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentuser(request):
    user = UserSerializer(request.user)
    return Response(user.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_post_user(request):
    user = request.user
    posts = user.post_set.all()
    serializer = PostSerializer(posts,many=True)
    return Response({f"{user} Posts":serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile,many=False)
    return Response({"Profile":serializer.data})



    




