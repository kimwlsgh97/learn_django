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
    return render(request, 'portfolio/corp_search.html', {"corps":corps,"ports":ports}) # 검색 완료 화면 출력
    
@login_required
def port(request):
    all_ports = Myport.objects.all()
    sectors = Sector.objects.all()
    port_corp = Mycorp.objects.all()

    if request.method == 'POST':
        
        # 회사 추가 기능
        stock_name = request.POST.get('stock_name')
        if stock_name:
            user = request.user
            stock_code = request.POST.get('stock_code')

            portname = request.POST.get('port')
            port = Myport.objects.get(username=user, portname=portname)

            info = Corp.objects.get(stock_name=stock_name)

            result = Mycorp.objects.filter(username=user, port=port, stock_name=stock_name)
            if not result:
                Mycorp.objects.create(username=user, port=port, stock_name=stock_name, stock_code=stock_code, info=info)
        
    return render(request,'portfolio/port.html', {"all_ports":all_ports, "sectors":sectors})

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
    return render(request, 'portfolio/port_new.html', {'form':form})

@login_required
def port_remove(request, pk):
    port = get_object_or_404(Myport, pk=pk)
    port.delete()
    return redirect('port')

@login_required
def sector_new(request, pk):
    port = get_object_or_404(Myport, pk=pk)
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
    return render(request, 'portfolio/sector_new.html', {'form':form, 'port':port})

@login_required
def sector_remove(request,pk):
    sector = get_object_or_404(Sector, pk=pk)
    sector.delete()
    return redirect('port')

@login_required
def add_corp_to_sector(request, pk):
    mycorp = Mycorp.objects.get(pk=pk)
    sector_name = request.POST.get('sector')
    sector = Sector.objects.get(sector_name=sector_name)
    if sector:
        print(sector, mycorp)
        mycorp.sector = sector
        mycorp.save()
    return redirect('port')

@login_required
def corp_remove(request,pk):
    corp = get_object_or_404(Mycorp, pk=pk)

    sector_name = corp.sector
    portname = corp.port

    sector_g = Sector.objects.get(sector_name=sector_name)
    port_g = Myport.objects.get(portname=portname)
    
    sector_price = sector_g.sector_price
    sector_price -= corp.info.stock_price

    port_price = port_g.port_price
    port_price -= corp.info.stock_price

    sector_f = Sector.objects.filter(sector_name=sector_name)
    port_f = Myport.objects.filter(portname=portname)

    sector_f.update(sector_price=sector_price)
    port_f.update(port_price=port_price)
    corp.delete()
    return redirect('port')

@login_required
def add_count(request):
    if request.method=='POST':
        count = request.POST.get('stock_count')
        corp_pk = request.POST.get('corp_pk')
        sector_pk = request.POST.get('sector_pk')
        port_pk = request.POST.get('port_pk')
        price = request.POST.get('stock_price')
        
        # corp = get_object_or_404(Mycorp, pk=pk)
        total_price = int(price) * int(count)     
        corp = Mycorp.objects.filter(pk=corp_pk)
        corp.update(stock_count=count, total_price=total_price)

        sector_g = Sector.objects.get(pk=sector_pk)
        sector_corps = Mycorp.objects.filter(sector=sector_g)

        sector_price = 0
        for corp in sector_corps:
            sector_price += corp.total_price
        
        sector_f = Sector.objects.filter(pk=sector_pk)
        sector_f.update(sector_price=sector_price)

        # 해당 회사가 속한 포트폴리오 가져오기
        port_g = Myport.objects.get(pk=port_pk)

        # 포트폴리오에 속한 종목 가져오기
        port_sectors = Sector.objects.filter(port=port_g)

        # 포트폴리오 총 금액 계산하기
        port_price = 0
        for sector in port_sectors:
            port_price += sector.sector_price

        # 업데이트하기위해 포트폴리오 쿼리셋 불러옴
        port_f = Myport.objects.filter(pk=port_pk)

        # 포트폴리오 총금액 저장
        port_f.update(port_price=port_price)
        
        
    return redirect('port')


def sector_update():
    sector_g = Sector.objects.get(pk=sector_pk)
    sector_corps = Mycorp.objects.filter(sector=sector_g)

    sector_price = 0
    for corp in sector_corps:
        sector_price += corp.total_price
    
    sector_f = Sector.objects.filter(pk=sector_pk)
    sector_f.update(sector_price=sector_price)





@login_required
def test(request):
    form = TestForm()
    if request.method == 'POST':
        # print(request.POST)
        user = request.user

        portname = request.POST.get('portname')
        port = Myport.objects.get(username=user, portname=portname)

        sector_name = request.POST.get('sector_name')
        sector = Sector.objects.get(username=user, sector_name=sector_name)

        stock_name = request.POST.get('stock_name')
        Mycorp.objects.filter(username=user, port=port, sector=sector,stock_name=stock_name).delete()
    return render(request, 'portfolio/test.html', {"form":form})

