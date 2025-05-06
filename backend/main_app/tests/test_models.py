from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Task, BulletinBoardMessage, Comment

class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create tasks, messages, and comments related to the user
        self.task = Task.objects.create(title='Task 1', description='Description for Task 1', completed=False, user=self.user)
        self.message = BulletinBoardMessage.objects.create(title='Message 1', content='Content for message 1', image='images/facebook.png', user=self.user)
        self.comment = Comment.objects.create(content='This is a comment on message 1', user=self.user, message=self.message)

    def test_user_create(self):
        # Check if the user is created successfully
        self.assertEqual(str(self.user), 'testuser')

    def test_task_create(self):
        # Check if task is created successfully
        self.assertEqual(str(self.task), 'Task 1')
        self.assertEqual(self.task.user, self.user)

    def test_bulletin_board_message_create(self):
        # Check if message is created successfully
        self.assertEqual(self.message.title, 'Message 1')
        self.assertEqual(self.message.user, self.user)

    def test_comment_create(self):
        # Check if comment is created successfully
        self.assertEqual(self.comment.content, 'This is a comment on message 1')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.message, self.message)

    # -------------------
    # Relationships
    # -------------------

    def test_task_user_relationship(self):
        # Check the relationship between task and user
        self.assertEqual(self.task.user.username, 'testuser')

    def test_comment_message_relationship(self):
        # Check the relationship between comment and message
        self.assertEqual(self.comment.message, self.message)

    # -------------------
    # Cascade Deletions
    # -------------------

    def test_deleting_user_cascades_to_task(self):
        # Test if deleting a user deletes related tasks
        self.assertEqual(Task.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Task.objects.count(), 0)
    
    def test_deleting_message_cascades_to_comment(self):
        # Test if deleting a message deletes related comments
        self.assertEqual(Comment.objects.count(), 1)
        self.message.delete()
        self.assertEqual(Comment.objects.count(), 0)

    # -------------------
    # Model Methods
    # -------------------

    def test_task_str_method(self):
        # Check if the string representation of task works correctly
        self.assertEqual(str(self.task), 'Task 1')

    def test_bulletin_board_message_str_method(self):
        # Check if the string representation of message works correctly
        self.assertEqual(str(self.message), 'Message 1')

    def test_comment_str_method(self):
        # Check if the string representation of comment works correctly
        self.assertEqual(str(self.comment), 'This is a comment on message 1')
