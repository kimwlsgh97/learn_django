from django.contrib import admin

# 정의한 모델 가져오기
from .models import Post, Corp

admin.site.register(Post)

admin.site.register(Corp)

# Register your models here.
