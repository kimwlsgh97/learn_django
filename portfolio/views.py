from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

# from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the port index>")

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'portfolio/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'portfolio/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'portfolio/post_edit.html', {'form':form})



def cr_post(author, title, text):
    Post.objects.create(author=author, title=title, text=text)

# def use_query(request):
    # posts = Post.objects.all()
    # users = User.objects.all()
    # post_ft = Post.objects.filter(published_date=None)
    # print("post_ft: ", post_ft)
    # print("posts: ", posts)
    # print("users: ", users)
    # or_up = Post.objects.order_by('create_date')
    # print("or_up: ", or_up)
    # or_dw = Post.objects.order_by('-create_date')
    # print("or_dw: ", or_dw)
    # me = User.objects.get(username='jinho')
    # title = 'Test - 2'
    # text = 'Test - 2'
    # cr_post(me, title, text)