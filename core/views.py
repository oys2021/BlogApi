from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.serializers import *
from core.models import *
from django.core.paginator import Paginator


def api_root(request):
    return render(request, 'core/api_home.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "GET":
        sort = request.GET.get("sort", "created_at")
        filter_category = request.GET.get("filter", "all")

        queryset = Post.objects.all()

        # Filtering
        if filter_category != "all":
            queryset = queryset.filter(category__slug=filter_category)

        # Sorting
        allowed_sorts = ["created_at", "view_count", "comment_count"]
        if sort in allowed_sorts:
            queryset = queryset.order_by(f"-{sort}")

        serializer = PostSerializer(queryset, many=True)
        return Response(
            {"success": True, "message": "Post results", "data": serializer.data},
            status=status.HTTP_200_OK
        )


    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "success": True,
                "message": "Post created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Invalid request input",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','GET'])
@permission_classes([IsAuthenticated])
def post_detail(request,pk):
    if request.method == "GET":

        post=Post.objects.get(pk=pk)

        serializer = PostSerializer(post)
        return Response(
            {"success":True, "message":"Post results","data":serializer.data},
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

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


    