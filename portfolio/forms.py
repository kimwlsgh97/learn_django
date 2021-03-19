# 폼을 불러오기
from django import forms

# 모델 불러오기
from .models import Post, Comment

# 폼만들기

# forms.ModelForm이 있어야 장고가 폼으로 인식한다.
class PostForm(forms.ModelForm):

    # 폼을 만들때 쓰이는 모델 지정
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)