from django.shortcuts import render,get_object_or_404
from .serializer import PostSerializer,CommentSerializer,ProfileSerializer,EventSerializer
from rest_framework.response import Response
from .models import Post,Comment,Event
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Profile
@api_view(['GET'])
def ApiOverview(request):
    apidocumentation = [
        'Posts/',
        'Get_By_Id/<str:pk>/',
        'Create_Post/',
        'Delete_Post/<str:pk>/',
        'Update_Post/<str:pk>/',
        'Like_Post/<str:pk>/',
        'dislike_Post/<str:pk>/',
        'comment/<str:pk>/',
        'comments/',
        'like_comment/<str:pk>/',
        'dislike_comment/<str:pk>/',
    ]
    return Response(apidocumentation)


@api_view(['GET'])
def Posts(request):
    post = Post.objects.all()
    serializer = PostSerializer(post,many=True)
    return Response({"Posts" : serializer.data}) 




@api_view(['GET'])
def Get_Posts_By_id(request,pk):
    post = Post.objects.get(pk=pk)
    serializer = PostSerializer(post,many=False)
    return Response({"Posts" : serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Create_Post(request):
    data = request.data
    serializer = PostSerializer(data=data)

    if serializer.is_valid():
        # Create the Post object using serializer.save()
        post = serializer.save(author=request.user)
        return Response({"Details": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"Error": "Information Not Valid", "Details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delete_Post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author != request.user :
        return Response({"Details":"Cannot Delete This Post"},status=status.HTTP_400_BAD_REQUEST)
    else:
        post.delete()
        return Response({"Details":"Post Deleted Successfully"},status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def Update_Post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"Details": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if post.author != request.user:
        return Response({"Details": "Cannot Update This Post"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    serializer = PostSerializer(instance=post, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        post.edited = True
        post.save()
        return Response({'Details': 'Post updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user in post.likers.all() and request.user not in post.dislikers.all():
        post.likers.remove(request.user)
        post.like_count = post.likers.count()
        
        return Response({'Like':'Post like removed'},status=status.HTTP_200_OK)
    else: 
        post.dislikers.remove(request.user)
        post.likers.add(request.user)
        return Response({'Like':'Post Liked'},status=status.HTTP_200_OK)
    

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user in post.dislikers.all() and request.user not in post.likers.all():
        post.dislikers.remove(request.user)
        return Response({'Like':'Post dislike removed'})
    else:
        post.likers.remove(request.user)
        post.dislikers.add(request.user)
        return Response({'Like':'Post disLiked'})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request,pk):
    post = get_object_or_404(Post, pk=pk)
    data = request.data
    serializer = CommentSerializer(data=data,many=False)
    if serializer.is_valid():
        comment = Comment.objects.create(
            author = request.user,
            parent_post = post,
            content = data['content'],
        )
        post.comments.add(comment)
        return Response({'comment':serializer.data})
    else:
        return Response({'Error':'Invalid post data'})
    

@api_view(['GET'])
def showallcomment(request):
    comment = Comment.objects.all()
    print(comment)
    serializer = CommentSerializer(comment,many=True)
    return Response({"comment":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    if request.user in comment.likers.all() and request.user not in comment.dislikers.all():
        comment.likers.remove(request.user)
        return Response({'Like':'comment like removed'})
    else: 
        comment.dislikers.remove(request.user)
        comment.likers.add(request.user)
        return Response({'Like':'comment Liked'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.dislikers.all() and request.user not in comment.likers.all():
        comment.dislikers.remove(request.user)
        return Response({'Like':'comment dislike removed'})
    else:
        comment.likers.remove(request.user)
        comment.dislikers.add(request.user)
        return Response({'Like':'comment disLiked'})
    
#added new
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    print(user)
    profile_instance = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile_instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    if not request.user.groups.filter(name='Admin').exists():
        return Response({"error": "You do not have permission to create events"}, status=status.HTTP_403_FORBIDDEN)

    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        return Response({"error": "You do not have permission to update events"}, status=status.HTTP_403_FORBIDDEN)

    event = get_object_or_404(Event, pk=pk)
    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        return Response({"error": "You do not have permission to delete events"}, status=status.HTTP_403_FORBIDDEN)

    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return Response({'Info':'Deleted'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Show_Event(request):
    if not request.user.groups.filter(name='Admin').exists():
        return Response({"error": "You do not have permission to delete events"}, status=status.HTTP_403_FORBIDDEN)
    
    Events = Event.objects.all()
    serializer = EventSerializer(Events,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Enroll_Event(request,pk):
    selected_event = get_object_or_404(Event,pk=pk)
    if request.method == 'POST':
        user = request.user
        if user in selected_event.enrolled_users.all() :
            return Response({"Info":"you already enrolled"},status=status.HTTP_302_FOUND)
        
        if selected_event.count == 0:
            return Response({"Info":"Places are completed"},status=status.HTTP_400_BAD_REQUEST)
        
        selected_event.enrolled_users.add(user)
        selected_event.count = selected_event.count - 1
        selected_event.save()
        return Response({"Info":"User Enrolled Seccuesfully"},status=status.HTTP_200_OK)
    else:
        return Response({"Info":"Method Is Not Post"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profiles(request):
    search_query = request.query_params.get('query', None)

    if not request.user.groups.filter(name='User').exists():
        return Response({"error": "You do not have permission to search profiles"}, status=status.HTTP_403_FORBIDDEN)

    if search_query:
        profiles = Profile.objects.filter(name__icontains=search_query)
    else:
        profiles = Profile.objects.all()

    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)