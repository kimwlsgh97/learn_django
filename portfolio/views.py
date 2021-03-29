from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Post, Comment, Myport, Sector, Mycorp, Corp
from .forms import PostForm, CommentForm, MyportForm, SectorForm, TestForm

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
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name') # POST 요청 확인
        if corp_name: # 회사 이름 있을때
            corps = Corp.objects.filter(stock_name__contains=corp_name) #회사 리스트 가져옴
            ports = Myport.objects.filter(username=request.user) # 내 포트폴리오 목록 불러옴
            sectors = Sector.objects.filter(username=request.user) # 내 섹터 목록 불러옴
    return render(request, 'portfolio/corp_search.html', {"corps":corps,"ports":ports, "sectors":sectors}) # 검색 완료 화면 출력
    
@login_required
def port(request):
    if request.method == 'POST':
        print(request.POST)
    error = False
    stock_name = request.POST.get('stock_name')
    if stock_name:
        user = request.user
        stock_code = request.POST.get('stock_code')

        portname = request.POST.get('port')
        port_g = Myport.objects.get(username=user, portname=portname)

        sector_name = request.POST.get('sector_name')
        sector_g = Sector.objects.get(username=user, sector_name=sector_name)
        
        result = Mycorp.objects.filter(username=user, port=port_g, sector=sector_g,stock_name=stock_name)
        if not result:
            Mycorp.objects.create(username=user, port=port_g, sector=sector_g, stock_name=stock_name, stock_code=stock_code)
        else:
            error = True

    myports = Myport.objects.filter(username=request.user)
    return render(request,'portfolio/port.html', {"ports":myports, "error":error})

@login_required
def port_new(request):
    if request.method == "POST":
        form = MyportForm(request.POST)
        if form.is_valid():
            port = form.save(commit=False)
            port.username = request.user
            port.save()
            return redirect('port')
    else:
        form = MyportForm()
    return render(request, 'portfolio/port_edit.html', {'form':form})

@login_required
def port_remove(request):
    if request.method == 'POST':
        # print(request.POST)
        user = request.user

        portname = request.POST.get('portname')
        port = Myport.objects.get(username=user, portname=portname)

        sector_name = request.POST.get('sector_name')
        sector = Sector.objects.get(username=user, sector_name=sector_name)

        stock_name = request.POST.get('stock_name')
        Mycorp.objects.filter(username=user, port=port, sector=sector,stock_name=stock_name).delete()

        
    return redirect('port')

@login_required
def sector_new(request, pk):
    port = Myport.objects.get(pk=pk)
    if(request.method == 'POST'):
        form = SectorForm(request.POST)
        if form.is_valid():
            sector = form.save(commit=False)
            sector.username = request.user
            sector.port = port
            sector.save()        
            return redirect('port')
    else:
        form = SectorForm()
    return render(request, 'portfolio/port_edit.html', {'form':form, 'port':port})






@login_required
def test(request):
    form = TestForm()
    return render(request, 'portfolio/test.html', {"form":form})

