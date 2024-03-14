from django.shortcuts import render,get_object_or_404
from .serializer import PostSerializer,CommentSerializer,ProfileSerializer
from rest_framework.response import Response
from .models import Post,Comment
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
    serializer = PostSerializer(data=data,many=False)
    print(serializer)
    if serializer.is_valid():
        Post.objects.create(**data,author=request.user)
        return Response({"Details":serializer.data},status=status.HTTP_201_CREATED)
    else :
        return Response({"Error":"Informations Not Valid"},status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delete_Post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author != request.user :
        return Response({"Details":"Cannot Delete This Post"},status=status.HTTP_400_BAD_REQUEST)
    else:
        post.delete()
        return Response({"Details":"Post Deleted Successfully"},status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Update_Post(request,pk):
    post = Post.objects.get(pk=pk)
    data = request.data
    if post.author != request.user:
        return Response({"Details":"Cannot Update This Post"},status=status.HTTP_400_BAD_REQUEST)
    else:
        post.content = data['content']
        post.edited = True
        post.save()
        return Response({'Details':'Post updated successfully'},status=status.HTTP_200_OK)

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
    


    

