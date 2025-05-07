from rest_framework import serializers
from .models import Task, BulletinBoardMessage, Comment
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        print(user, "testing user in serializer")
        return user



class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only field for the username
    created_at = serializers.DateTimeField(read_only=True)  # Read-only field for the creation date
    completed = serializers.BooleanField(default=False)  # Default value for completed field

    class Meta:
        model = Task
        fields = '__all__'



class BulletinBoardMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BulletinBoardMessage
        fields = ['id', 'title', 'content', 'image', 'created_at', 'user']
        extra_kwargs = {'user': {"read_only": True}}  # Make user read-only


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'message']

