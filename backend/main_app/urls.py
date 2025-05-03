from django.urls import path
from .views import TaskListCreate, BulletinBoardMessageListCreate, CommentListCreate,CreateUserView,LoginView,RegisterView, HomeListCreate


urlpatterns = [
    path('api/tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('api/bulletin-board-messages/', BulletinBoardMessageListCreate.as_view(), name='bulletin-board-message-list-create'),
    path('api/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('api/Home/', HomeListCreate.as_view(), name='home-list-create'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
    path('accounts/', include('django.contrib.auth.urls')), 

]
