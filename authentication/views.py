from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from authentication.models import CustomUser
from authentication.serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data= request.data
    serializer=UserSerializer(data=data,context={'request':request})

    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "message":"User registered successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "message":"Invalid Request ","details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_user(request,pk):
    data=request.data
    user = CustomUser.objects.get(pk=pk)
    serializer= UserSerializer(user,data=data,partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success":True,"data":serializer.data},
            status=status.HTTP_200_OK
        )
    
    return Response(
        {"success": False, "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user=CustomUser.objects.filter(username=request.user.username)
    serializer= UserProfileSerializer(user,many=True)
    return Response(
            {"success":True,"data":serializer.data},
            status=status.HTTP_200_OK
    )
    
    