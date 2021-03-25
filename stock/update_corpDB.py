from pykrx import stock
import sqlite3
import pandas as pd
from datetime import datetime, date

# 평일에만 업데이트 하도록 하기
def isnew():
    today = date.today()
    week = today.weekday()

    if(week <5):
        inputDB()
    else:
        print("장 운영시간이 아님.")


# corp db에 저장
def inputDB():
    # krx 사용 df 정보 스크랩
    df, tickers, names = useKrx()

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
def useKrx():
    now = useDate()
    names = []

    print(now, "의 데이터를 가져옵니다.")
    # 티커 가져옴
    tickers = stock.get_market_ticker_list(now, market="KOSPI")
    for ticker in tickers:
        # 이름 가져옴
        names.append(stock.get_market_ticker_name(ticker))

    # 주가 가져옴
    df = stock.get_market_ohlcv_by_ticker(now)

    # 주가, 회사이름 반환
    return df, tickers, names


# 스크랩을 위한 현재시간 가져오는 함수
def useDate():
    now = datetime.now()
    return now.strftime('%Y%m%d')


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

isnew()
