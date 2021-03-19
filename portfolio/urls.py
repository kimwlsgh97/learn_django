from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

# ''(공백) 이면  views.post_list() 실행
urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', views.index, name='index'),
    # post문자를 포함/정수값을 받아 pk라는 이름으로 view에 전달/ '/'가 나옴
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publih'),
    path('post/(<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]