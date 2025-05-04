from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task, BulletinBoardMessage, Comment
from .serializers import TaskSerializer, BulletinBoardMessageSerializer, CommentSerializer, UserSerializer


# View for JWT Token creation (Login)
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)  # Authenticate the user
            print(f"Authenticated user: {user}", username, password)  # Debugging line
            try:
                if user:
                    print(f"User logged in: ", user)  # Debugging line
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    content = {'refresh': str(refresh), 'access': access_token, 'user': UserSerializer(user).data}
                    return Response(content, status=status.HTTP_200_OK)
            except Exception as err:
                print(str(err))
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View for creating a new user and returning JWT tokens
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get('username') or not request.data.get('password'):
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = super().create(request, *args, **kwargs)
            user = User.objects.get(username=response.data['username'])
            refresh = RefreshToken.for_user(user)
            content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data}
            return Response(content, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View for Task CRUD operations
class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# View for Bulletin Board Message CRUD operations
class BulletinBoardMessageListCreate(generics.ListCreateAPIView):
    queryset = BulletinBoardMessage.objects.all()
    serializer_class = BulletinBoardMessageSerializer

# View for Comment CRUD operations
class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class VerifyUserView(APIView):
    def get(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
