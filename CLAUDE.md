# CLAUDE.md — 개인 사진 갤러리 웹 애플리케이션

## 프로젝트 개요
소프트웨어공학 (INC4119) 팀 프로젝트. 사용자가 사진을 업로드하고, 다른 사용자가 사진을 볼 수 있으며, 사용자 간 다이렉트 메시지를 주고받을 수 있는 웹 기반 사진 갤러리 애플리케이션.

**제출 기한: 2026년 6월 14일 (일요일)**

## 기술 스택
- Backend: Python 3, FastAPI, SQLAlchemy (ORM), PostgreSQL 18.4
- Frontend: React + Vite, Axios
- 인증: JWT (python-jose)
- 파일 업로드: python-multipart
- 비밀번호: bcrypt 해시 저장
- DB: PostgreSQL (localhost:5432, DB명: photogallery)
- 실행 환경: Windows, 서버 + 클라이언트 동일 PC

## 폴더 구조
```
photo-gallery/
├── backend/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py             # DB 연결, 세션 관리
│   ├── models/
│   │   ├── user.py             # User 모델
│   │   ├── photo.py            # Photo 모델
│   │   └── message.py          # Message 모델
│   ├── routes/
│   │   ├── auth.py             # 회원가입, 로그인, 로그아웃
│   │   ├── users.py            # 사용자 목록 조회
│   │   ├── photos.py           # 사진 CRUD, 검색
│   │   └── messages.py         # DM 전송, 수신함, 답장, 삭제
│   ├── schemas/                # Pydantic 스키마 (요청/응답)
│   ├── dependencies.py         # JWT 인증 의존성
│   ├── .env                    # DATABASE_URL, SECRET_KEY
│   ├── venv/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   ├── MainPage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   └── MessagesPage.jsx
│   │   └── components/
│   │       ├── PhotoCard.jsx
│   │       ├── SearchBar.jsx
│   │       └── MessageItem.jsx
│   └── package.json
├── uploads/                    # 업로드된 사진 저장 디렉토리
├── .gitignore
├── CLAUDE.md
└── README.md
```

## API 명세

### 인증
```
POST /api/auth/signup
  Body: { username, password }
  Response: { id, username }

POST /api/auth/login
  Body: { username, password }
  Response: { access_token, token_type }

POST /api/auth/logout
  Headers: Authorization: Bearer <token>
  Response: { message }
```

### 사용자
```
GET /api/users
  인증: 불필요
  Response: [{ id, username }]
```

### 사진
```
GET /api/photos
  인증: 필요
  Response: [{ id, user_id, username, image_url, description, keywords, created_at }]

POST /api/photos
  인증: 필요
  Body: multipart/form-data (file, description, keywords)
  Response: { id, image_url, description, keywords }

PUT /api/photos/{id}
  인증: 필요 (본인만)
  Body: { description, keywords }
  Response: { id, description, keywords }

GET /api/photos/search?keyword=
  인증: 불필요
  Response: [{ id, user_id, username, image_url, description, keywords, created_at }]
```

### 다이렉트 메시지
```
POST /api/messages
  인증: 필요
  Body: { receiver_id, content }
  Response: { id, sender_id, receiver_id, content, created_at }

GET /api/messages
  인증: 필요
  Response: [{ id, sender_id, sender_username, content, parent_id, created_at, is_read }]

POST /api/messages/{id}/reply
  인증: 필요
  Body: { content }
  Response: { id, sender_id, receiver_id, content, parent_id, created_at }

DELETE /api/messages/{id}
  인증: 필요
  Response: { message }
```

## DB 모델 (SQLAlchemy)

### User
```python
class User(Base):
    id: Integer, PK, autoincrement
    username: String, unique, not null
    password_hash: String, not null
    created_at: DateTime, default=now
```

### Photo
```python
class Photo(Base):
    id: Integer, PK, autoincrement
    user_id: Integer, FK(users.id), not null
    image_path: String, not null
    description: String, nullable
    keywords: String, nullable  # 쉼표로 구분된 키워드
    created_at: DateTime, default=now
```

### Message
```python
class Message(Base):
    id: Integer, PK, autoincrement
    sender_id: Integer, FK(users.id), not null
    receiver_id: Integer, FK(users.id), not null
    content: String, not null
    parent_id: Integer, FK(messages.id), nullable  # 답장 시 원본 메시지 참조
    is_read: Boolean, default=False
    created_at: DateTime, default=now
```

## 기능 요구사항 (6가지 — 추가 기능 구현 금지)

1. **회원가입 / 로그인 / 로그아웃** — JWT 기반 인증
2. **로그인 사용자** — 사용자 목록 + 모든 사진 조회 가능
3. **비로그인 사용자** — 사용자 목록만 조회 (사진 열람 불가)
4. **사진 업로드/수정** — 설명 + 키워드 포함, 수정은 설명/키워드만 (본인만)
5. **키워드 검색** — 키워드로만 검색 (텍스트/유저 검색 구현 금지)
6. **다이렉트 메시지** — 모든 게시물에 DM 버튼, 수신함, Reply/Delete 버튼

## 개발 규칙

### 절대 하지 말 것
- 명세에 없는 추가 기능 구현 (감점 대상)
- 텍스트 검색, 유저 검색 구현
- 좋아요, 댓글, 팔로우 등 추가 기능
- 사진 파일 자체 수정 (설명/키워드만 수정 가능)

### 반드시 할 것
- 비밀번호는 bcrypt 해시 저장 (passwordHash)
- DM 버튼은 모든 사진 게시물에 표시
- 수신 메시지에 Reply / Delete 버튼 필수
- 사진 수정 버튼은 게시물 소유자에게만 표시
- 비로그인 시 사진 조회 불가, 사용자 목록만 조회 가능
- CORS 설정 (프론트: localhost:5173, 백: localhost:8000)

### 코드 스타일
- Python: snake_case, type hint 사용 권장
- 커밋 메시지: 한국어 또는 영어, prefix 사용 (feat:, fix:, docs:, style:, chore:)
- 환경변수는 .env 파일 사용, 코드에 하드코딩 금지

## 실행 방법

### 백엔드
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload      # http://localhost:8000
```

### 프론트엔드
```bash
cd frontend
npm install
npm run dev                    # http://localhost:5173
```

### PostgreSQL
```bash
psql -U postgres
# DB 생성: CREATE DATABASE photogallery;
```

### .env 파일 (backend/.env)
```
DATABASE_URL=postgresql://postgres:비밀번호@localhost:5432/photogallery
SECRET_KEY=your-secret-key-here
```

## 주요 의존성

### Backend (requirements.txt)
```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose[cryptography]
python-multipart
python-dotenv
bcrypt
passlib[bcrypt]
```

### Frontend (package.json)
```
react
react-dom
react-router-dom
axios
```

## 현재 진행 상황
- [x] GitHub 레포 생성
- [x] PostgreSQL 설치 및 DB 생성
- [x] 백엔드 가상환경 세팅
- [x] 과제 #1 유스케이스/테스트케이스 제출완료
- [x] 과제 #2 UML 설계 제출완료
- [ ] FastAPI 백엔드 코드 작성 ← 지금 여기
- [ ] React 프론트엔드 코드 작성
- [ ] 프론트/백엔드 통합 테스트
- [ ] 과제 #3 테스트 리포트 작성
- [ ] YouTube 사용자 매뉴얼 영상 제작
- [ ] README.md 작성
- [ ] GitHub 최종 push