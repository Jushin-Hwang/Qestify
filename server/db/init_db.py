# server/db/init_db.py
import os
import sys
import pymysql
from dotenv import load_dotenv

# ⚠️ app.py에 있는 DB 연결 정보와 동일하게 입력해주세요.
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# 실행할 SQL 명령어 (테이블이 이미 존재하면 에러가 나지 않도록 IF NOT EXISTS 추가)
CREATE_TABLE_COMMAND = """
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    answers TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DROP_TABLE_COMMAND = "DROP TABLE IF EXISTS applications;"

def get_db_connection():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            db = 'questify',
            charset='utf8'
        )
        
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def execute_db_command(command) :
    conn= None
    try:
        print("데이터베이스에 연결하는 중...")
        conn = get_db_connection()
        print("연결됨")
        cur = conn.cursor()
        print("SQL 명령어 실행 중...")
        cur.execute(command)
        conn.commit()
        cur.close()
        print("명령어가 성공적으로 실행되었습니다.")
    except Exception as error:
        print(f"오류 발생: {error}")
    finally:
        if conn is not None:
            conn.close()
            print("데이터베이스 연결이 종료되었습니다.")

def initialize_database():
    """ 'applications' 테이블을 생성합니다. """
    print("=== 테이블 생성 시작 ===")
    execute_db_command(CREATE_TABLE_COMMAND)

def drop_table():
    """ 'applications' 테이블을 삭제합니다. """
    print("=== 테이블 삭제 시작 ===")
    execute_db_command(DROP_TABLE_COMMAND)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        drop_table()
    else:
        initialize_database()