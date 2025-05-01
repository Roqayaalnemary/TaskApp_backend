from rest_framework import serializers
from .models import User, Task, BulletinBoardMessage, Comment,Home


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # جعل كلمة المرور "للكتابة فقط" للـ API

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



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