import pymysql
DB_CONFIG = dict(
    host = "localhost",
    user = "root" ,
    password="123",
    database="convindb",
    charset="utf8"
)

class DB:
    def __init__(self,**config):
        self.config = config
    
    def connect(self):
        return pymysql.connect(**self.config) #딕셔너리 전개
    
    #로그인 검증
    def verify_user(self, username, password):
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,(username, password))
                #SELECT는 행 단위로 가져온다. fetchone 의 결과는 튜플
                count, = cur.fetchone()
                return count == 1
            
    #상품 전체 조회
    def fetch_inventory(self):
        sql = "SELECT id, name, amount, price, Ocost FROM inventory ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
            

    # 자산 조회
    def fetch_bal(self):
        with self.connect() as conn:  # self.connect()는 DB 연결 메서드
            with conn.cursor() as cur:
                cur.execute("SELECT bal FROM balance")
                row = cur.fetchone()  # 한 행 가져오기
                if row:
                    return row[0]  # bal 값
                return 0  # 값 없으면 0 반환

            
    #수량 증가
    def add_amount(self, name, amount):

        sql = "UPDATE inventory SET amount = (SELECT amount FROM (SELECT amount FROM inventory WHERE name=%s) AS sub) + %s WHERE name=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (name, amount, name))
                    conn.commit()
                    return True
            except Exception:
                conn.rollback()
                return False
    # 수량 감소
    def subtract_amount(self, name, amount):
        sql = "UPDATE inventory SET amount = (SELECT amount FROM (SELECT amount FROM inventory WHERE name=%s) AS sub) - %s WHERE name=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (name, amount, name))
                    conn.commit()
                    return True
            except Exception:
                conn.rollback()
                return False
            
    # 잔액 증가
    def add_balance(self, amount):
        sql = "UPDATE balance SET bal = bal + %s WHERE id = 1"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (amount,))
                    conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    # 잔액 감소 
    def subtract_balance(self, amount):
        sql = "UPDATE balance SET bal = bal - %s WHERE id = 1"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (amount,))
                    conn.commit()
                    return True
            except Exception:
                conn.rollback()
                return False
            
    # 특정 상품의 발주가 가져오기
    def fetch_Ocost(self, name):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Ocost FROM inventory WHERE name=%s", (name,))
                row = cur.fetchone()
                if row:
                    return row[0]  # 발주가
                return None
            
        # 특정 상품의 발주가 가져오기
    def fetch_price(self, name):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT price FROM inventory WHERE name=%s", (name,))
                row = cur.fetchone()
                if row:
                    return row[0]  # 발주가
                return None

    def fetch_amount(self, name):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT amount FROM inventory WHERE name=%s", (name,))
                row = cur.fetchone()
                if row:
                    return row[0]  # 발주가
                return None

