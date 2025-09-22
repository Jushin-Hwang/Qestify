# app.py

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2 # PostgreSQL 연동을 위한 라이브러리
from dotenv import load_dotenv

from google.cloud import storage
from werkzeug.utils import secure_filename

import io, csv

load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
CORS(app)

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

@app.route('/api/applications', methods = ['GET'])
def get_applications() :
    conn = None
    try :
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, contact, TO_CHAR(created_at, 'YYYY-MM-DD'), answers FROM applications ORDER BY created_at DESC")

        applications = []
        columns = [desc[0] for desc in cur.description]
        for row in cur.fetchall() :
            applications.append(dict(zip(columns, row)))

        cur.close()
        return jsonify(applications)
    
    except (Exception, psycopg2.DatabaseError) as error :
        return jsonify({'success' : False, 'message' : str(error)}), 500
    finally :
        if conn is not None :
            conn.close()

@app.route('/api/export_csv', methods = ['GET'])
def export_csv() :
    conn = None
    try :
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, contact, TO_CHAR(created_at, 'YYYY-MM-DD'), answers, image_url FROM applications ORDER BY id ASC")

        applications = []
        columns = [desc[0] for desc in cur.description]
        for row in cur.fetchall() :
            applications.append(dict(zip(columns, row)))

        cur.close()
        
        return jsonify(applications)
    
    except (Exception, psycopg2.DatabaseError) as error :
        return jsonify({'success' : False, 'message' : str(error)}), 500
    finally :
        if conn is not None :
            conn.close()


@app.route('/api/submit', methods = ['POST'])
def submit_application() :
    # ⬇️ 아래 두 줄을 추가해주세요!
    print("--- 받은 텍스트 데이터 ---")
    print(request.form)
    print("--- 받은 파일 데이터 ---")
    print(request.files)
    conn = None
    try :
        name = request.form['name']
        contact = request.form['contact']
        answers_json = request.form['answers']
        answers = json.loads(answers_json)

        file = request.files.get('fan_photo')

        image_url = None
        if file : 
            storage_client = storage.Client()

            bucket_name = os.getenv('GCS_BUCKET_NAME')
            bucket = storage_client.bucket(bucket_name)

            filename = secure_filename(file.filename)
            blob = bucket.blob(filename)

            blob.upload_from_file(
                file,
                content_type = file.content_type
            )

            image_url = blob.public_url

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        sql = """
            INSERT INTO applications (name, contact, answers, image_url)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        cur.execute(sql, (name, contact, json.dumps(answers), image_url))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            'success': True, 
            'message': '신청서가 성공적으로 제출되었습니다.',
            'application_id': new_id
        })
    
    except (Exception, psycopg2.DatabaseError) as error :
        print(f"An error occurred : {error}")
        return jsonify({'success' : False, 'message' : str(error)}), 500
    finally :
        if conn is not None :
            conn.close()

# 서버 실행 (python app.py로 직접 실행할 경우)
if __name__ == '__main__':
    # debug=True는 개발 중에만 사용하며, 코드 변경 시 서버가 자동 재시작됩니다.
    app.run(port=5000, debug=True)