# app.py

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv

from werkzeug.utils import secure_filename

import io, csv

load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv('DATABASE_URL')

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

@app.route('/api/applications', methods = ['GET'])
def get_applications() :
    conn = None
    try :
        conn = get_db_connection()
        cur = conn.cursor() # 결과를 딕셔너리 형태로 받기 위해 dictionary=True 추가
        # contact 컬럼이 제거되었으므로 SELECT 문에서 제외합니다.
        cur.execute("SELECT id, name, answers FROM applications ORDER BY created_at DESC")

        applications = cur.fetchall()
        print(applications)
        cur.close()
        print("성공적으로 보냈습니다.")
        return jsonify(applications)
    
    except Exception as error :
        return jsonify({'success' : False, 'message' : str(error)}), 500
    finally :
        if conn is not None :
            conn.close()

@app.route('/api/submit', methods = ['POST'])
def submit_application() :
    conn = None
    try :
        # name과 answers만 받도록 수정합니다.
        name = request.form['name']
        answers = request.form['answers']

        conn = get_db_connection()
        cur = conn.cursor()

        # contact와 image_url을 INSERT 문에서 제거합니다.
        sql = """
            INSERT INTO applications (name, answers)
            VALUES (%s, %s);
        """
        cur.execute(sql, (name, answers))
        
        new_id = cur.lastrowid # MySQL에서 마지막으로 삽입된 ID를 가져옵니다.
        conn.commit()
        cur.close()
        
        return jsonify({
            'success': True, 
            'message': '신청서가 성공적으로 제출되었습니다.',
            'application_id': new_id
        })
    
    except Exception as error :
        print(f"An error occurred : {error}")
        return jsonify({'success' : False, 'message' : str(error)}), 500
    finally :
        if conn is not None :
            conn.close()

# 서버 실행 (python app.py로 직접 실행할 경우)
if __name__ == '__main__':
    # debug=True는 개발 중에만 사용하며, 코드 변경 시 서버가 자동 재시작됩니다.
    app.run(host = '0.0.0.0', port=5000, debug=True)