from django.urls import path
from . import views

# ''(공백) 이면  views.post_list() 실행
urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', views.index, name='index'),
    # post문자를 포함/정수값을 받아 pk라는 이름으로 view에 전달/ '/'가 나옴
    path('post/<pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
]