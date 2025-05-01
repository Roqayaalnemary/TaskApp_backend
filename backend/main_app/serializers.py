from rest_framework import serializers
from .models import User, Task, BulletinBoardMessage, Comment,Home


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'user']


class BulletinBoardMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletinBoardMessage
        fields = ['id', 'title', 'content', 'image', 'created_at', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'message']

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['id', 'title', 'description', 'banner_image', 'created_at', 'user']