from django.urls import path
from .views import TaskListCreate, BulletinBoardMessageListCreate, CommentListCreate

urlpatterns = [
    path('api/tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('api/bulletin-board-messages/', BulletinBoardMessageListCreate.as_view(), name='bulletin-board-message-list-create'),
    path('api/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('api/Home/', HomeListCreate.as_view(), name='home-list-create'),
]

