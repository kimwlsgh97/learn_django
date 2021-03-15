from django.contrib import admin

# 정의한 모델 가져오기
from .models import Post

admin.site.register(Post)

# Register your models here.
