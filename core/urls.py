from django.urls import path

from .views import *

urlpatterns=[
    path("posts/",posts,name="post"),
    path("posts/<int:pk>/",post_detail,name="post-detail"),
    path('categories/',category_list, name="categories"),
    path('tags/',tag_list,name="tags"),
    path('posts/<int:post_id>/comments/', PostCommentListCreateView.as_view(), name='post-comments'),
    path("notifications/unread/", UnreadNotificationListView.as_view(), name="unread-notifications"),
    path("notifications/<int:pk>/read/", MarkNotificationAsReadView.as_view(), name="mark-as-read"),
]
