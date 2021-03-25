# 회사 정보 초기화
from update_corpDB import useDB, useDate

now = useDate()

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
        WHERE stock_name=(?)""", (corp[0],corp[1],corp[2],corp[3],corp[4],corp[5],corp[6],corp[7],corp[8],corp[8],now))

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
    
    for corp in corps:
        # 이미 존재하는 회사라면 업데이트
        try:
            cur.execute("SELECT stock_name FROM portfolio_corp WHERE stock_name=(?)",(corp[8],))
            upCorp(corp,cur)
        except:
            setCorp(corp,cur)

        # 초기 DB 저장
        # setCorp(corp,cur)

        # jango DB 비우기
        # deleteAll(corp, cur)
        
    con.commit()
    print("djangoDB 업데이트 완료")


updating()