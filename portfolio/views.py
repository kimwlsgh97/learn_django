from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django.utils import timezone
# from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the port index>")

def index(request):
    posts = Post.objects.all()
    return render(request, 'portfolio/index.html', {'message':posts})

def post_list(request):
    msg = 'Post_list'
    return render(request, 'portfolio/post_list.html', {'message':msg})

def cr_post(author, title, text):
    Post.objects.create(author=author, title=title, text=text)

def use_query(request):
    posts = Post.objects.all()
    users = User.objects.all()
    post_ft = Post.objects.filter(published_date=None)
    print("post_ft: ", post_ft)
    print("posts: ", posts)
    print("users: ", users)
    or_up = Post.objects.order_by('create_date')
    print("or_up: ", or_up)
    or_dw = Post.objects.order_by('-create_date')
    print("or_dw: ", or_dw)
    me = User.objects.get(username='jinho')
    title = 'Test - 2'
    text = 'Test - 2'
    cr_post(me, title, text)