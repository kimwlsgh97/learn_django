from django.contrib import admin

# 정의한 모델 가져오기
from .models import Post, Comment, Myport, Sector, Mycorp

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Myport)

admin.site.register(Sector)

admin.site.register(Mycorp)

# Register your models here.
