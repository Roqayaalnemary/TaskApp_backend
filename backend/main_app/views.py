from rest_framework import generics
from .models import User, Task, BulletinBoardMessage, Comment, Home
from .serializers import UserSerializer, TaskSerializer, BulletinBoardMessageSerializer, CommentSerializer, HomeSerializer
from django.contrib.auth import authenticate

class LoginView(APIView):

  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        refresh = RefreshToken.for_user(user)
        content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
        return Response(content, status=status.HTTP_200_OK)
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
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

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            user = User.objects.get(username=response.data['username'])
            refresh = RefreshToken.for_user(user)  # إنشاء RefreshToken و AccessToken
            content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data}
            return Response(content, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
