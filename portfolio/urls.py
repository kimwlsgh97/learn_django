
from django.urls import path
from . import views

# ''(공백) 이면  views.post_list() 실행
urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.index, name='index'),
]