# from django.contrib import admin

from django.contrib import admin
from .models import Task, BulletinBoardMessage, Comment

# تسجيل النماذج في لوحة التحكم
admin.site.register(Task)
admin.site.register(BulletinBoardMessage)
admin.site.register(Comment)

