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
from .forms import PostForm, CommentForm, MyportForm, SectorForm, CashForm

# from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the port index>")


def main(request):
    return render(request, 'portfolio/main.html')

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
def port_edit(request, pk):
    edit = True
    port_g = get_object_or_404(Myport, pk=pk)
    if request.method == "POST":
        form = MyportForm(request.POST, instance=port_g)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('port')
    else:
        form = MyportForm(instance=port_g)        

    return render(request, 'portfolio/port_edit.html', {'port':port_g, 'edit':edit, 'form':form})

@login_required
def cash_edit(request, pk):
    port_g = get_object_or_404(Myport, pk=pk)
    if request.method == "POST":
        form = CashForm(request.POST, instance=port_g)

        # 폼에서 정보 받아오기 전에 이전 정보 불러오기 (is_valid 전에)
        pre_port_price = port_g.port_price
        pre_cash_price = port_g.cash_price
        
        if form.is_valid():
            cash_price = int(form.cleaned_data['cash_price'])
            now_port_price = pre_port_price - pre_cash_price + cash_price
            cash = form.save(commit=False)
            cash.port_price = now_port_price
            cash.save()
        return redirect('port')
    else:
        form = CashForm(instance=port_g)
    return render(request, 'portfolio/cash_edit.html', {'port':port_g, 'form': form})

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
    if request.method=='POST':
        mycorp = Mycorp.objects.get(pk=pk)

        port_pk = request.POST.get('port_pk')
        port = Myport.objects.get(pk=port_pk)

        sector_name = request.POST.get('sector')

        sector = Sector.objects.get(port=port,sector_name=sector_name)
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
        stock_count = request.POST.get('stock_count')
        corp_pk = request.POST.get('corp_pk')
        # sector_pk = request.POST.get('sector_pk')
        # port_pk = request.POST.get('port_pk')
        stock_price = request.POST.get('stock_price')
        
        mycorp = Mycorp.objects.filter(pk=corp_pk)
        mycorp_g = Mycorp.objects.get(pk=corp_pk)
        now_total_price = int(stock_price) * int(stock_count)
        pre_total_price = mycorp_g.total_price
        mycorp.update(stock_count=stock_count, total_price=now_total_price)

        sector_pk = mycorp_g.sector.pk
        sector = Sector.objects.filter(pk=sector_pk)
        sector_g = Sector.objects.get(pk=sector_pk)
        # 기존의 종목금액 - 이전 회사 종목금액 + 현재 회사 종목금액
        sector_price = sector_g.sector_price - pre_total_price + now_total_price
        sector.update(sector_price=sector_price)

        port_pk = mycorp_g.port.pk
        port = Myport.objects.filter(pk=port_pk)
        port_g = Myport.objects.get(pk=port_pk)
        port_price = port_g.port_price - pre_total_price + now_total_price
        port.update(port_price=port_price)
        
        
    return redirect('port')

@login_required
def change_sector(request, pk):
    corp_g = get_object_or_404(Mycorp,pk=pk)
    if request.method == "POST":
        form_sector = request.POST.get('sector')
        pre_sector = Sector.objects.get(sector_name=corp_g.sector)
        now_sector = Sector.objects.get(sector_name=form_sector)

        pre_sector_price = pre_sector.sector_price - corp_g.total_price
        now_sector_price = now_sector.sector_price + corp_g.total_price

        p_sector = Sector.objects.filter(sector_name=corp_g.sector)
        n_sector = Sector.objects.filter(sector_name=form_sector)
        corp = Mycorp.objects.filter(pk=pk)

        p_sector.update(sector_price=pre_sector_price)
        n_sector.update(sector_price=now_sector_price)
        corp.update(sector=now_sector)
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