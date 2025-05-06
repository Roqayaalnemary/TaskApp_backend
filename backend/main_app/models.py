from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField() 
    completed = models.BooleanField(default=False) 
    priority = models.CharField(max_length=1, choices=[('h', 'High'), ('m', 'Medium'), ('l', 'Low')], default='m')
    recurrence = models.CharField(max_length=10, choices=[('none', 'No Recurrence'), ('d', 'Daily'), ('w', 'Weekly'), ('m', 'Monthly')], default='none')
    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 


    def __str__(self):
        return self.title
        from django.db import models



class BulletinBoardMessage(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField() 
    image = models.CharField(max_length=200)  
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    message = models.ForeignKey(BulletinBoardMessage, on_delete=models.CASCADE)  

    def __str__(self):
        return self.content[:50] 


        


        