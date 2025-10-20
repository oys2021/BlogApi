from django.urls import path
from .views import *

urlpatterns = [
    path("", APIHomeView.as_view(), name="api-root"),
    path("posts/", PostListCreateView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostRetrieveUpdateView.as_view(), name="post-detail"),
    path('categories/', CategoryListView.as_view(), name="category-list"),
    path('tags/', TagListView.as_view(), name="tag-list"),
    path('posts/<int:post_id>/comments/', PostCommentListCreateView.as_view(), name='post-comments'),
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/unread/", UnreadNotificationListView.as_view(), name="unread-notifications"),
    path("notifications/<int:pk>/read/", MarkNotificationAsReadView.as_view(), name="mark-notification-read"),
]