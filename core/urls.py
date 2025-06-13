from django.urls import path

from .views import *

urlpatterns=[
    path("posts/",posts,name="post"),
    path("posts/<int:pk>/",post_detail,name="post-detail")
]