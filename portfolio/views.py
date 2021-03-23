from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Post, Comment, Myport, Sector, Mycorp, Corp
from .forms import PostForm, CommentForm

# from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the port index>")

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'portfolio/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'portfolio/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'portfolio/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST ,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'portfolio/post_edit.html', {'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'portfolio/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'portfolio/add_comment_to_post.html', {'form':form})


def corp_search(request):
    stock_name = request.POST['corp_name'] # POST 요청 확인
    if stock_name: # 회사 이름 있을때
        corps = Corp.objects.filter(stock_name__contains=stock_name) #회사 리스트 가져옴

    return render(request, 'portfolio/corp_search.html', {"corps":corps})

@login_required    
def add_to_me(request):
    if request.method == "POST":
        stock_name = request.POST['stock_name']
        corp = Mycorp.objects.filter(stock_name=stock_name)
        if corp:
            return redirect('myport')
        else:
            stock_code = request.POST['stock_code']
            Mycorp.objects.create(author=request.user, stock_code=stock_code,stock_name=stock_name, created_date=timezone.now())
    else:
        print("에러코드 : 000001")
    return redirect('myport')


@login_required
def myport(request):
    corps = Mycorp.objects.filter(author=request.user)
    stocks = []
    for corp in corps:
        stocks.append(Corp.objects.filter(stock_name=corp.stock_name))

    return render(request, "portfolio/myport.html",{"stocks":stocks})

@login_required
def add_count(request, pk):
    corp = get_object_or_404(Mycorp, pk=pk)
    if request.method == "POST":
        corp.stock_count = request.POST['stock_count']
        corp.save()
    return redirect('myport')



@login_required
def port_remove(request, pk):
    corp = get_object_or_404(Mycorp, pk=pk)
    corp.delete()
    return redirect('myport')
