from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

# ''(공백) 이면  views.post_list() 실행
urlpatterns = [
    path('', views.port, name='port'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),

    path('corp/search/', views.corp_search, name='corp_search'),

    path('port/', views.port, name='port'),
    path('port/new/', views.port_new, name='port_new'),
    path('port/<int:pk>/remove/', views.port_remove, name='port_remove'),
    path('port/<int:pk>/edit/', views.port_edit, name='port_edit'),

    path('sector/<int:pk>/new/', views.sector_new, name='sector_new'),
    path('sector/<int:pk>/add_corp/', views.add_corp_to_sector, name='add_corp_to_sector'),
    path('sector/<int:pk>/remove/', views.sector_remove, name='sector_remove'),
    path('sector/<int:pk>/edit/', views.sector_edit, name='sector_edit'),

    path('corp/<int:pk>/remove', views.corp_remove, name='corp_remove'),
    path('corp/add_count', views.add_count, name='add_count'),

    path('cash/<int:pk>/edit/', views.port_edit, name='cash_edit'),
]