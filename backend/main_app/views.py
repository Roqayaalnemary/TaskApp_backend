from rest_framework import generics, serializers, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task, BulletinBoardMessage, Comment
from .serializers import TaskSerializer, BulletinBoardMessageSerializer, CommentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


# View for JWT Token creation (Login)
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            try:
                if user:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    content = {'refresh': str(refresh), 'access': access_token, 'user': UserSerializer(user).data}
                    return Response(content, status=status.HTTP_200_OK)
            except Exception as err:
                print(str(err))
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            print(f"Error occurred: {err}")
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View for creating a new user and returning JWT tokens
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        print(f"Received request data: {request.data}") 
        if not request.data.get('username') or not request.data.get('password'):
            print("Missing username or password")  
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = super().create(request, *args, **kwargs) 
            user = User.objects.get(username=response.data['username'])
            refresh = RefreshToken.for_user(user)
            content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data}
            return Response(content, status=status.HTTP_201_CREATED)
        except Exception as err:
            print(f"Error occurred: {err}") 
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyUserView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    try:
        user = User.objects.get(username=request.user.username)
        try:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        except Exception as token_error:
            return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            date_str = request.query_params.get('date')
            queryset = Task.objects.all()
            if date_str:  # إذا كان هناك تاريخ مرفق في الطلب
                queryset = queryset.filter(date__date=date_str)  # فلترة المهام حسب التاريخ فقط (بدون وقت)
            print(queryset, "queryset")  # Debugging line
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            try :
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as err:
                print(f"Error occurred: {str(err)}")  # Debugging line
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskDetail(APIView):
#   permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer


    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            serializer = self.serializer_class(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            print(str(err))
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BulletinBoardMessageListCreate(generics.ListCreateAPIView):
    queryset = BulletinBoardMessage.objects.all()
    serializer_class = BulletinBoardMessageSerializer

    def get(self, request):
        try:
            queryset = BulletinBoardMessage.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            print(request.user)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(f"Invalid data: {serializer.errors}")  # Debugging line
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(str(err))
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetail(APIView):
    serializer_class = BulletinBoardMessageSerializer
    lookup_field = 'id'

    def put(self, request, post_id):
        try:
            post = BulletinBoardMessage.objects.get(id=post_id)
            serializer = self.serializer_class(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, post_id):
        try:
            post = BulletinBoardMessage.objects.get(id=post_id)
            post.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            print(str(err))
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View for Comment CRUD operations
class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer















# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Task
# from .serializers import TaskSerializer

# class TaskListView(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
