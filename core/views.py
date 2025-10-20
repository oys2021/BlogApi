from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers import *
from core.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import generics
from django.shortcuts import get_object_or_404
from core.models import PostView
from django.db.models import F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from rest_framework.views import APIView
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class APIHomeView(APIView):
    def get(self, request):
        return render(request, 'core/api_home.html')

class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        sort = self.request.GET.get("sort", "created_at")
        filter_category = self.request.GET.get("filter", "all")

        allowed_sorts = ["created_at", "view_count", "comment_count"]
        if sort not in allowed_sorts:
            sort = "created_at"

        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments')

        if filter_category != "all":
            if Category.objects.filter(slug=filter_category).exists():
                queryset = queryset.filter(category__slug=filter_category)

        return queryset.order_by(f"-{sort}")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        page_number = request.GET.get('page', 1)
        paginator = Paginator(queryset, 20)
        
        try:
            posts_page = paginator.page(page_number)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)

        serializer = self.get_serializer(posts_page, many=True)
        return Response({
            "success": True,
            "message": "Post results",
            "data": serializer.data,
            "pagination": {
                "current_page": posts_page.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count
            }
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)

            try:
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
            except Exception as e:
                logger.error(f"WebSocket broadcast failed: {e}")

            return Response({
                "success": True,
                "message": "Post created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Invalid request input",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments')

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        with transaction.atomic():
            view, created = PostView.objects.get_or_create(
                user=user,
                post=post,
                defaults={'user': user, 'post': post}
            )
            
            if created:
                Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
                post.refresh_from_db()

        serializer = self.get_serializer(post)
        return Response({
            "success": True,
            "message": "Post results",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        
        if post.author != request.user:
            return Response({
                "success": False,
                "message": "You don't have permission to edit this post"
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Post updated successfully"
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success": False,
            "message": "Invalid request input",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class TagListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class PostCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent=None).select_related('user', 'post').order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['post'] = post
        return context

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related('user').order_by('-created_at')[:10]

class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            notificationreadstatus__user=self.request.user,
            notificationreadstatus__read=False
        ).select_related('user').order_by('-created_at')

class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

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