# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255) 

    def __str__(self):
        return self.name

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



class Home(models.Model):
    title = models.CharField(max_length=255, default="Welcome to Task Manager")  # عنوان الصفحة الرئيسية
    description = models.TextField(default="Here you can manage tasks, check messages, and interact with comments.")  # وصف الصفحة الرئيسية
    banner_image = models.ImageField(upload_to='home_banners/', null=True, blank=True)  # صورة البانر
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ربط الصفحة بالمستخدم

    def __str__(self):
        return f"Home Page for {self.user.name}"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


