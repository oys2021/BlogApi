from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Category, Tag, Post, PostTag, Comment, Like
from authentication.serializers import *

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['id', 'post', 'tag']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content',
            'author', 'category', 'category_id',
            'tags', 'tag_ids', 'is_featured',
            'view_count', 'comment_count',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent', write_only=True, required=False, allow_null=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'post_id',
            'author', 'parent_id', 'replies',
            'created_at', 'updated_at'
        ]

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post')

    class Meta:
        model = Like
        fields = ['id', 'user', 'post_id', 'created_at']
