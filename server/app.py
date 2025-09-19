# app.py

import os
from flask import Flask
import psycopg2 # PostgreSQL 연동을 위한 라이브러리

# Flask 앱 생성
app = Flask(__name__)

# DB 연결 설정 (실제 정보는 환경 변수 등으로 관리하는 것이 안전합니다)
# 예: DATABASE_URL = "postgresql://db_user:db_password@localhost:5432/my_database"
DATABASE_URL = "YOUR_DATABASE_CONNECTION_STRING"

# 데이터베이스와 연결을 시도하는 함수 (예시)
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# 서버가 잘 켜졌는지 확인하는 테스트 API
@app.route('/')
def hello():
    # DB 연결 테스트
    conn = get_db_connection()
    if conn:
        conn.close()
        return '서버가 정상적으로 동작하고, DB에도 연결할 수 있습니다!'
    else:
        return '서버는 동작하지만, DB 연결에 실패했습니다. 설정을 확인하세요.'


# 서버 실행 (python app.py로 직접 실행할 경우)
if __name__ == '__main__':
    # debug=True는 개발 중에만 사용하며, 코드 변경 시 서버가 자동 재시작됩니다.
    app.run(port=5000, debug=True)