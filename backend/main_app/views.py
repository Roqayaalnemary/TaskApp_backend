from rest_framework import generics
from .models import User, Task, BulletinBoardMessage, Comment, Home
from .serializers import UserSerializer, TaskSerializer, BulletinBoardMessageSerializer, CommentSerializer, HomeSerializer

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class BulletinBoardMessageListCreate(generics.ListCreateAPIView):
    queryset = BulletinBoardMessage.objects.all()
    serializer_class = BulletinBoardMessageSerializer

class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class HomePageList(generics.ListCreateAPIView):
    queryset = Home.objects.all()  # جلب جميع البيانات من نموذج Home
    serializer_class = HomeSerializer  # استخدام السيرياليزر لتمثيل البيانات

