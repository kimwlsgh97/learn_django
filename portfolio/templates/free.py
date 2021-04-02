POST = {
    'stock_price': '10000',
    'stock_count': '10',
    'pk': 'mycorp.pk'
}

mycorp = Mycorp.objects.filter(pk=pk)
mycorp_g = Mycorp.objects.get(pk=pk)
now_total_price = int(stock_price) * int(stock_count)
pre_total_price = mycorp_g.total_price
mycorp.update(total_price=now_total_price)

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


섹터금액 - 이전금액 + 지금금액