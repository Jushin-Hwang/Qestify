# Questify (퀘스티파이) ✨

**지루한 설문지는 이제 그만\! 사용자의 경험을 퀘스트로 만드는 동적 설문조사 플랫폼**

Questify는 한 번에 하나의 질문에만 집중하게 하여 사용자의 이탈률을 줄이고, 부드러운 화면 전환과 인터랙티브한 UI를 통해 설문 경험을 즐거운 퀘스트처럼 만드는 풀스택 웹 애플리케이션입니다.

<br>

## 📜 프로젝트 설명

이 프로젝트는 전통적인 방식의 길고 지루한 신청서 폼을 개선하고자 시작되었습니다. 사용자가 각 문항에 완전히 몰입할 수 있도록 전체 화면을 활용하고, 답변과 동시에 다음 문항으로 넘어가는 동적인 경험을 제공합니다.

FC서울 팬 이벤트 신청서를 예시로 구현하였으며, 텍스트 입력부터 파일 첨부, 관리자 페이지를 통한 신청 내역 관리 및 CSV 데이터 추출 기능까지 완전한 서비스 플로우를 갖추고 있습니다.

<br>

## 🚀 주요 기능

  * **동적 질문 흐름**: 한 화면에 하나의 질문만 노출하여 사용자 집중도 향상
  * **부드러운 화면 전환**: 답변 시 다음 문항으로 자동 스크롤되는 애니메이션
  * **다양한 입력 유형 지원**: 주관식(text), 객관식(button), 리스트(select), 파일 첨부 등
  * **클라우드 파일 저장**: GCP Cloud Storage와 연동하여 이미지 파일을 안정적으로 관리
  * **관리자 대시보드**: 제출된 모든 신청 내역을 실시간으로 확인
  * **데이터 추출**: 전체 신청 내역을 CSV 파일로 한번에 다운로드

<br>

## 🛠️ 기술 스택

| 구분 | 기술 |
| :--- | :--- |
| **Frontend** | `HTML`, `CSS`, `Vanilla JavaScript` |
| **Backend** | `Python`, `Flask`, `Flask-CORS` |
| **Database** | `PostgreSQL` on **GCP Cloud SQL** |
| **File Storage** | **GCP Cloud Storage** |
| **Infra** | `Git`, `GitHub` |

<br>

## ⚙️ 시작하기

### 1\. 프로젝트 복제

```bash
git clone https://github.com/Jushin-Hwang/Questify_with_Gemini.git
cd Questify_with_Gemini
```

### 2\. 백엔드 설정

1.  **가상 환경 생성 및 활성화**

    ```bash
    cd server
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```

2.  **라이브러리 설치**

    ```bash
    pip install -r requirements.txt
    ```

    *(만약 `requirements.txt` 파일이 없다면, `pip freeze > requirements.txt` 명령어로 생성해주세요.)*

3.  **`.env` 파일 설정**
    `server` 폴더에 `.env` 파일을 생성하고 아래 내용을 채워주세요.

    ```env
    # .env.example
    DATABASE_URL="postgresql://postgres:YOUR_DB_PASSWORD@YOUR_GCP_IP:5432/postgres"
    GCS_BUCKET_NAME="YOUR_GCP_BUCKET_NAME"
    GOOGLE_APPLICATION_CREDENTIALS="server/your-gcp-key-file.json"
    ```

4.  **데이터베이스 초기화**

    ```bash
    python db/init_db.py
    ```

5.  **서버 실행**

    ```bash
    python app.py
    ```

### 3\. 프론트엔드 실행

1.  VS Code에서 `client/index.html` 파일을 우클릭합니다.
2.  `Open with Live Server`를 선택하여 사용자용 신청서 페이지를 엽니다.
3.  관리자 페이지는 `client/admin/admin.html` 파일을 Live Server로 열어 확인합니다.

# Qestify
설문조사 및 참가신청 응답 Server와 Client 페이지를 작성한 Demo 프로젝트입니다.