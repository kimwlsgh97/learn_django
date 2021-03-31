from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

# ''(공백) 이면  views.post_list() 실행
urlpatterns = [
    path('', views.port, name='port'),
    # path('', views.index, name='index'),
    # post문자를 포함/정수값을 받아 pk라는 이름으로 view에 전달/ '/'가 나옴
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    path('corp/search/', views.corp_search, name='corp_search'),

    path('port/', views.port, name='port'),
    path('port/new/', views.port_new, name='port_new'),
    path('port/<int:pk>/remove/', views.port_remove, name='port_remove'),

    path('sector/<int:pk>/new/', views.sector_new, name='sector_new'),
    path('sector/<int:pk>/add_corp/', views.add_corp_to_sector, name='add_corp_to_sector'),
    path('sector/<int:pk>/remove/', views.sector_remove, name='sector_remove'),
    path('sector/<int:pk>/edit/', views.sector_edit, name='sector_edit'),

    path('corp/<int:pk>/remove', views.corp_remove, name='corp_remove'),
    path('corp/add_count', views.add_count, name='add_count'),
]