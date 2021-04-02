# 폼을 불러오기
from django import forms

# 모델 불러오기
from .models import Post, Comment, Myport, Sector, Mycorp

# 폼만들기
class TestForm(forms.Form):
    test = forms.CharField(label='test')
# forms.ModelForm이 있어야 장고가 폼으로 인식한다.
class PostForm(forms.ModelForm):

    # 폼을 만들때 쓰이는 모델 지정
    class Meta:
        model = Post
        fields = ('title', 'text',)
        labels = {
            'title':'제목',
            'text':'내용'
        }
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class MyportForm(forms.ModelForm):

    class Meta:
        model = Myport
        fields = ('portname',)
        labels = {
            'portname': '이름'
        }

class CashForm(forms.ModelForm):

    class Meta:
        model = Myport
        fields = ('cash_price', 'cash_per')
        labels = {
            'cash_price': '보유금액',
            'cash_per':'목표 현금 비중'
        }


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('sector_name', 'sector_per',)
        labels = {
            'sector_name':'종목 이름',
            'sector_per': '목표 비중(%)'
        }

# class CountForm(forms.ModelForm):

#     class Meta:
#         model = Mycorp
#         fields = ('stock_count',)








