from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# 회원가입 폼 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
# from django.urls import reverse_lazy
# from django.views import generic

from django.contrib.auth.models import User
from .models import Post, Comment, Myport, Sector, Mycorp, Corp
from .forms import PostForm, CommentForm, MyportForm, SectorForm, TestForm



# from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the port index>")


def corp_search(request):
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name') # POST 요청 확인
        if corp_name: # 회사 이름 있을때
            corps = Corp.objects.filter(stock_name__contains=corp_name) #회사 리스트 가져옴
            ports = Myport.objects.filter(username=request.user) # 내 포트폴리오 목록 불러옴
    return render(request, 'portfolio/corp_search.html', {"corps":corps,"ports":ports}) # 검색 완료 화면 출력
    
@login_required
def port(request):
    all_ports = Myport.objects.filter(username=request.user)
    sectors = Sector.objects.all()
    port_corp = Mycorp.objects.all()

    if request.method == 'POST':
        print(request.POST)
        # 회사 추가 기능
        stock_name = request.POST.get('stock_name')
        if stock_name:
            user = request.user
            stock_code = request.POST.get('stock_code')
            portname = request.POST.get('port')

            port = Myport.objects.get(username=user, portname=portname)

            info = Corp.objects.get(stock_code=stock_code)

            result = Mycorp.objects.filter(username=user, port=port, stock_code=stock_code)
            if not result:
                # 내 회사 추가
                Mycorp.objects.create(username=user, port=port, stock_name=stock_name, stock_code=stock_code, info=info)
        
    return render(request,'portfolio/port.html', {"all_ports":all_ports, "sectors":sectors})

@login_required
def port_new(request):
    if request.method == "POST":
        portname = request.POST.get('portname')
        cash_price = request.POST.get('cash_price')
        cash_per = request.POST.get('cash_per')
        Myport.objects.create(username=request.user, portname=portname, port_price=cash_price, cash_price=cash_price, cash_per=cash_per)
        return redirect('port')
    return render(request, 'portfolio/port_new.html')

@login_required
def port_edit(request, pk):
    edit = True
    port_g = get_object_or_404(Myport, pk=pk)
    if request.method == "POST":
        port_f = Myport.objects.filter(pk=pk)
        portname = request.POST.get('portname')
        cash_price = request.POST.get('cash_price')
        cash_per = request.POST.get('cash_per')

        intCash = int(cash_price)

        port_price = port_g.port_price - port_g.cash_price + intCash

        port_f.update(portname=portname, port_price=port_price, cash_price=cash_price, cash_per=cash_per)
        return redirect('port')
        

    return render(request, 'portfolio/port_edit.html', {'port':port_g, 'edit':edit})

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
    return render(request, 'portfolio/sector_edit.html', {'form':form, 'port':port})

@login_required
def sector_edit(request, pk):
    edit = True
    sector = get_object_or_404(Sector, pk=pk)
    if(request.method == 'POST'):
        form = SectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()      
            return redirect('port')
    else:
        form = SectorForm(instance=sector)
    return render(request, 'portfolio/sector_edit.html', {'form':form, 'port':port, 'edit':edit})

@login_required
def sector_remove(request,pk):
    sector = get_object_or_404(Sector, pk=pk)
    
    port = Myport.objects.filter(sectors=sector)
    port_g = Myport.objects.get(sectors=sector)

    sector_price = sector.sector_price
    port_price = port_g.port_price

    result = port_price - sector_price

    port.update(port_price=result)

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
    if(sector_name):
        sector_g = Sector.objects.get(sector_name=sector_name)
        sector_price = sector_g.sector_price
        sector_price -= corp.info.stock_price*corp.stock_count
        sector_f = Sector.objects.filter(sector_name=sector_name)
        sector_f.update(sector_price=sector_price)

    portname = corp.port    
    port_g = Myport.objects.get(portname=portname)
    port_price = port_g.port_price
    port_price -= corp.info.stock_price*corp.stock_count
    port_f = Myport.objects.filter(portname=portname)
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





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/signup.html', {'form':form})