from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.serializers import *
from core.models import *


def api_root(request):
    return render(request, 'core/api_home.html')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "GET":
        post= Post.objects.all()
        serializer= PostSerializer(post, many=True)

        return Response(
            {"success":True, "message":"Post results","data":serializer.data},
            status=status.HTTP_200_OK
        )
    
    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                {"success": True, "message": "Post created succcessfully"},
                status=status.HTTP_201_CREATED
            )

        print("Serializer Errors:", serializer.errors)

        return Response(
            {
                "success": False,
                "message": "invalid request input",
                "errors": serializer.errors  
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT','GET'])
@permission_classes([AllowAny])
def post_detail(request,pk):
    if request.method == "GET":

        post=Post.objects.get(pk=pk)

        serializer = PostSerializer(post)
        return Response(
            {"success":False, "message":"Post results","data":serializer.data},
            status=status.HTTP_200_OK
        )
    
    if request.method == "PUT":

        data= request.data

        serializer= PostSerializer( data=data, partial=True)

        if serializer.is_valid():
            return Response(
                    {"success":True, "message":"Post updated succcessfully"},
                    status= status.HTTP_200_OK
            )
        return Response(
                    {"success":False, "message":"invalid request input"},
                    status= status.HTTP_400_BAD_REQUEST
        )
    return Response(
         {"success":False, "message":"resource not found"},
         status= status.HTTP_404_NOT_FOUND
    )

    





    