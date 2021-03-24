from pykrx import stock
import sqlite3
import pandas as pd
from datetime import datetime

def useDate():
    now = datetime.now()
    return now.strftime('%Y%m%d')

def useKrx():
    today = useDate()
    names = []

    # 티커 가져옴
    tickers = stock.get_market_ticker_list(today, market="KOSPI")
    for ticker in tickers:
        # 이름 가져옴
        names.append(stock.get_market_ticker_name(ticker))

    # 주가 가져옴
    df = stock.get_market_ohlcv_by_ticker("20210323")

    # 주가, 회사이름 반환
    return df, tickers, names

def useDB():
    path = "test.sqlite3"
    con = sqlite3.connect(path)
    cur = con.cursor()
    return con, cur

def inputDB():
    # krx 사용 df 정보 스크랩
    df, tickers, names = useKrx()

    # DB연결
    con, cur = useDB()

    # df DB에 저장
    df.to_sql('test', con, if_exists='replace')

    # test 테이블에 회사이름을 넣을 column을 만들어준다.
    alterDB(con, cur)

    # ticker로 DB에 이름 붙여주기
    for i, name in enumerate(names):
        cur.execute("UPDATE test SET 이름=(?) WHERE 티커=(?)",(name,tickers[i]))
    con.commit()

def add_name():
    # krx 사용 df 정보 스크랩
    df, names = useKrx()

    # DB연결
    con, cur = useDB()
    
    # names DB에 저장 / 중복 검사 
    for name in names:
        cur.execute("SELECT name FROM name WHERE name=(?)",(name,))
        stock = cur.fetchall()
        if stock:
            continue
        else:
            cur.execute("INSERT INTO name(name) VALUES(?)",(name,))
    
    con.commit()




def createTable(con, cur, table_name, column_names, column_types):
    sql = """CREATE TABLE ? (
        idx INTEGER PRIMARY KEY,
        ? ?
    );"""
    data = (table_name,column_names, column_types)
    cur.execute(sql, data)
    con.commit()

def alterDB(con, cur):
    # 회사이름 DB에 추가
    cur.execute("ALTER TABLE test ADD 이름 varchar(20);")
    con.commit()

def readTicker():
    con, cur = useDB()
    cur.execute("SELECT 티커, 시가 FROM test;")
    # cur.execute("INSERT INTO table(,) VALUES ("%s","%s")")
    ticker = cur.fetchall()
    print(ticker)
    
# add_name()
inputDB()
# readTicker()


# df = usekrx()
# print(df)
# print(df.head(3))