from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField() 
    completed = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

class BulletinBoardMessage(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField() 
    image = models.ImageField(upload_to='images/')  
    created_at = models.DateTimeField(auto_now_add=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    message = models.ForeignKey(BulletinBoardMessage, on_delete=models.CASCADE)  

    def __str__(self):
        return self.content[:50] 



