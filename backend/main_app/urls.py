from django.urls import path, include
from .views import TaskListCreate, BulletinBoardMessageListCreate, CommentListCreate,CreateUserView,LoginView,VerifyUserView, TaskDetail, PostDetail





# from .views import create_task, create_comment


urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:task_id>/', TaskDetail.as_view(), name='task-detail'),
    path('posts/', BulletinBoardMessageListCreate.as_view(), name='bulletin-board-message-list-create'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='task-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]