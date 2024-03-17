from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def OverView(request):
    api = [
        {   
            "Endpoint":"/api/",
            "body":{"body":""},
            "METHOD":"GET",
            "Description":"This endpoint take you to another documentation for authentication"
        },
        {
            "Endpoint":"/api/posts/",
            "body":{"body":""},
            "METHOD":"GET",
            "Description":"this endpoint take you to another documentation for the functions of this system"
        }
    ]
    return Response(api)
