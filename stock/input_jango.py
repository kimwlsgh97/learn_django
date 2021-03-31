# 회사 정보 초기화
from update_corpDB import useDB

from datetime import datetime

nowDate = datetime.now()
now = nowDate.strftime("%Y%m%d")
# now = "20210101"

# 새로운 회사 정보 저장
def setCorp(corp, cur):
    cur.execute("""INSERT INTO portfolio_corp (
        stock_code, 
        stock_price, 
        high_price, 
        low_price, 
        end_price, 
        sell_count, 
        sell_price, 
        updown,
        stock_name,
        updated_date
        ) VALUES (?,?,?,?,?,?,?,?,?,?)""", (corp[0],corp[1],corp[2],corp[3],corp[4],corp[5],corp[6],corp[7],corp[8],now))

# 기조의 회사 정보 수정
def upCorp(corp, cur):
    cur.execute("""UPDATE portfolio_corp SET 
        stock_code=(?), 
        stock_price=(?), 
        high_price=(?), 
        low_price=(?), 
        end_price=(?), 
        sell_count=(?), 
        sell_price=(?), 
        updown=(?),
        stock_name=(?),
        updated_date=(?)
        WHERE stock_name=(?)""", (corp[0],corp[1],corp[2],corp[3],corp[4],corp[5],corp[6],corp[7],corp[8],now,corp[8]))

# 기조의 회사 정보 수정
def deleteAll(corp, cur):
    cur.execute("DELETE FROM portfolio_corp WHERE stock_name=(?)", (corp[8],))


# 회사 정보 업데이장
def updating():
    # corp DB 불러옴
    con, cur = useDB('corp.sqlite3')
    cur.execute("SELECT * FROM corp;")
    corps = cur.fetchall()
    con.close()
    
    con, cur = useDB('db.sqlite3')

    # print(corps)
    
    for corp in corps:
        # 이미 존재하는 회사라면 업데이트
        cur.execute("SELECT stock_name FROM portfolio_corp WHERE stock_name=(?)",(corp[8],))
        result = cur.fetchall()
        if result:
            print(corp[8], "업데이트 중")
            upCorp(corp,cur)
        else:
            print(corp[8], "생성 중")
            setCorp(corp,cur)

        # 초기 DB 저장
        # setCorp(corp,cur)

        # jango DB 비우기
        # deleteAll(corp, cur)
        
    con.commit()
    con.close()

    print("djangoDB에 적용 완료")


updating()