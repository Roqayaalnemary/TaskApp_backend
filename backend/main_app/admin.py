# from django.contrib import admin

from django.contrib import admin
from .models import Task, BulletinBoardMessage, Comment, Home

# تسجيل النماذج في لوحة التحكم
admin.site.register(Task)
admin.site.register(BulletinBoardMessage)
admin.site.register(Comment)
admin.site.register(Home)  # تسجيل النموذج الخاص بالصفحة الرئيسية

