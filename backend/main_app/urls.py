from django.urls import path, include
from django.urls import path
from .views import TaskListCreate, BulletinBoardMessageListCreate, CommentListCreate,CreateUserView,LoginView


urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('bulletin-board-messages/', BulletinBoardMessageListCreate.as_view(), name='bulletin-board-message-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    # path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

]
