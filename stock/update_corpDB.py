from pykrx import stock
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def beforeDay(today, num):
    result = today - timedelta(days=num)
    return result

    
# 평일에만 업데이트 하도록 하기
def update():
    now = datetime.now()
    week = now.weekday()
    year = now.year
    month = now.month
    day = now.day
    time = now.time()

    print('now', now)
    print('year', year)
    print('month', month)
    print('week', week)
    print('day', day)
    print('time', time)

    if(week <5):
        print("평일")

        # 장 시간 검사 위한 변수 선언
        # st_time = datetime(year, month, day, 9)
        ed_time = datetime(year, month, day, 15, 30)       
        
        # 15:30 이전이면 전날 기준으로 크롤링
        if (now < ed_time):
            print("장중 입니다.")
            # 월요일이면 3일전 금요일 지정
            if week == 0:
                fnDate = beforeDay(now, 3)
            else:
                # 하루 전날 지정하기
                fnDate = beforeDay(now, 1)

            inputDB(fnDate.strftime("%Y%m%d"))
        else:
            inputDB(now.strftime("%Y%m%d"))
    else:
        print("주말")
        if(week == 5):
            fnDate = beforeDay(now, 1)
        elif(week == 6):
            fnDate = beforeDay(now, 2)
        inputDB(now.strftime("%Y%m%d"))


# corp db에 저장
def inputDB(now):
    # krx 사용 df 정보 스크랩
    df, tickers, names = useKrx(now,"KOSPI")

    # test.sqlite3 DB연결
    con, cur = useDB("corp.sqlite3")

    # df내용 corp DB에 저장 (존재하면 삭제후 재생성)
    df.to_sql('corp', con, if_exists='replace')

    # test 테이블에 회사이름을 넣을 column을 만들어준다.
    alterDB(con, cur)

    # ticker로 DB에 이름 붙여주기
    for i, name in enumerate(names):
        cur.execute("UPDATE corp SET 이름=(?) WHERE 티커=(?)",(name,tickers[i]))
    con.commit()
    print("corpDB에 저장완료.")


# krx 스크랩
def useKrx(now, market):
    names = []

    print(now,"날짜의", market, "데이터를 가져옵니다.")
    # 티커 가져옴
    tickers = stock.get_market_ticker_list(now, market=market)
    for ticker in tickers:
        # 이름 가져옴
        names.append(stock.get_market_ticker_name(ticker))

    # 주가 가져옴
    df = stock.get_market_ohlcv_by_ticker(now)

    # 주가, 회사이름 반환
    return df, tickers, names


# db접속 함수
def useDB(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    return con, cur


# 이름 컬럼 생성 함수
def alterDB(con, cur):
    # 회사이름 DB에 추가
    cur.execute("ALTER TABLE corp ADD 이름 varchar(20);")
    con.commit()

# 이 함수로 불려졌을때 실행

update()
