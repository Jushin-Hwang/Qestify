# app.py

import os
import json
from flask import Flask, request, jsonify
import psycopg2 # PostgreSQL 연동을 위한 라이브러리
from dotenv import load_dotenv

load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')

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

@app.route('/api/submit', methods=['POST'])
def submit_application():
    # 1. 프론트엔드에서 보낸 JSON 데이터를 받습니다.
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '데이터가 없습니다.'}), 400

    conn = None
    try:
        # 2. 필수 데이터(이름, 연락처, 답변)가 모두 있는지 확인합니다.
        name = data['name']
        contact = data['contact']
        answers = data['answers'] # 이것은 딕셔너리 또는 리스트 형태일 것입니다.

        # 3. 데이터베이스에 연결합니다.
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 4. SQL INSERT 명령어를 준비합니다.
        # ⚠️ 중요: SQL 인젝션 공격을 방지하기 위해 반드시 %s 파라미터를 사용해야 합니다.
        sql = """
            INSERT INTO applications (name, contact, answers)
            VALUES (%s, %s, %s) RETURNING id;
        """
        # answers는 JSON 타입이므로, json.dumps를 사용해 문자열로 변환해줍니다.
        cur.execute(sql, (name, contact, json.dumps(answers)))
        
        # 5. DB에 변경사항을 확정하고, 새로 생성된 데이터의 id를 가져옵니다.
        new_id = cur.fetchone()[0]
        conn.commit()

        # 6. 연결을 종료하고 성공 메시지를 반환합니다.
        cur.close()
        
        return jsonify({
            'success': True, 
            'message': '신청서가 성공적으로 제출되었습니다.',
            'application_id': new_id
        })

    except (Exception, psycopg2.DatabaseError) as error:
        # 7. 오류가 발생하면 에러 메시지를 반환합니다.
        return jsonify({'success': False, 'message': str(error)}), 500
    finally:
        # 8. 모든 작업이 끝나면 DB 연결을 항상 닫아줍니다.
        if conn is not None:
            conn.close()

# 서버 실행 (python app.py로 직접 실행할 경우)
if __name__ == '__main__':
    # debug=True는 개발 중에만 사용하며, 코드 변경 시 서버가 자동 재시작됩니다.
    app.run(port=5000, debug=True)