from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
        # Create a new user using the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

# View for User Registration
class RegisterView(APIView):
    def post(self, request):
        # Handle user registration
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"msg": "User Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for JWT Token creation (Login)
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)  # Authenticate the user
            
            if user:
                # If authentication is successful, create JWT tokens
                refresh = RefreshToken.for_user(user)
                content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data}
                return Response(content, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Serializer for user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# View for creating a new user and returning JWT tokens
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
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

# View for Home Page CRUD operations
class HomePageList(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
