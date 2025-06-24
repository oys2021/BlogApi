from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.serializers import *
from core.models import *
from django.core.paginator import Paginator
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Count
from core.models import PostView
from django.db.models import F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from rest_framework.views import APIView





def api_root(request):
    return render(request, 'core/api_home.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "GET":
        sort = request.GET.get("sort", "created_at")
        filter_category = request.GET.get("filter", "all")

        queryset = Post.objects.all()

        
        if filter_category != "all":
            queryset = queryset.filter(category__slug=filter_category)


        
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
            post = serializer.save(author=request.user)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "chat_posts",  
                {
                    "type": "broadcast_message",
                    "message": {
                        "title": "New Post Created",
                        "body": f"{request.user.username} published '{post.title}'",
                        "post_id": post.id
                    }
                }
            )

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
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {"success": False, "message": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        user = request.user

        if not PostView.objects.filter(user=user, post=post).exists():
            PostView.objects.create(user=user, post=post)
            Post.objects.filter(pk=pk).update(view_count=F('view_count') + 1)

        serializer = PostSerializer(post)
        return Response(
            {"success": True, "message": "Post results", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Post updated successfully"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "message": "Invalid request input", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
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




class PostCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent=None).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['post'] = post
        return context
    



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Notification.objects.order_by('-created_at')[:10]


class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            notificationreadstatus__user=self.request.user,
            notificationreadstatus__read=False
        ).order_by('-created_at')
    

class MarkNotificationAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            status_obj = NotificationReadStatus.objects.get(
                user=request.user, notification_id=pk
            )
            status_obj.read = True
            status_obj.read_at = timezone.now()
            status_obj.save()
            return Response({"detail": "Marked as read."}, status=status.HTTP_200_OK)
        except NotificationReadStatus.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)