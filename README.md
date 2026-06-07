# Photo Gallery

소프트웨어공학 (INC4119) 팀 프로젝트 — 사진 업로드, 갤러리 탐색, 사용자 간 다이렉트 메시지를 지원하는 웹 기반 사진 갤러리 애플리케이션입니다.

---

## 기능

| # | 기능 | 설명 |
|---|------|------|
| 1 | 회원가입 / 로그인 / 로그아웃 | JWT 기반 인증 |
| 2 | 사진 갤러리 | 로그인 사용자만 전체 사진 조회 가능 |
| 3 | 사용자 목록 | 비로그인 사용자도 조회 가능 |
| 4 | 사진 업로드 / 수정 | 설명·키워드 포함, 수정은 본인만 가능 |
| 5 | 키워드 검색 | 키워드로 사진 검색 (로그인 불필요) |
| 6 | 다이렉트 메시지 | 모든 게시물에 DM 버튼, 수신함에서 Reply / Delete |

---

## 기술 스택

**Backend**
- Python 3 / FastAPI
- SQLAlchemy (ORM) + PostgreSQL 18.4
- JWT 인증 (`python-jose`), bcrypt 비밀번호 해시

**Frontend**
- React 19 + Vite
- React Router v7, Axios

---

## 프로젝트 구조

```
photo-gallery/
├── backend/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── database.py          # DB 연결 / 세션
│   ├── config.py            # 업로드 디렉토리 설정
│   ├── dependencies.py      # JWT 인증 의존성
│   ├── models/
│   │   ├── user.py
│   │   ├── photo.py
│   │   └── message.py
│   ├── routes/
│   │   ├── auth.py          # 회원가입, 로그인, 로그아웃
│   │   ├── users.py         # 사용자 목록
│   │   ├── photos.py        # 사진 CRUD, 검색
│   │   └── messages.py      # DM 전송, 수신함, 답장, 삭제
│   ├── schemas/             # Pydantic 스키마
│   ├── .env                 # 환경변수 (DB URL, SECRET_KEY)
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
└── uploads/                 # 업로드된 사진 저장
```

---

## 실행 방법

### 사전 요구사항

- Python 3.10+
- Node.js 18+
- PostgreSQL 18.4 (로컬 실행, 포트 5432)

### 1. PostgreSQL DB 생성

```sql
psql -U postgres
CREATE DATABASE photogallery;
```

### 2. 환경변수 설정

`backend/.env` 파일을 생성합니다.

```env
DATABASE_URL=postgresql://postgres:비밀번호@localhost:5432/photogallery
SECRET_KEY=your-secret-key-here
```

### 3. 백엔드 실행

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload    # http://localhost:8000
```

### 4. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

---

## API 명세

### 인증

| Method | Endpoint | 인증 | 설명 |
|--------|----------|------|------|
| POST | `/api/auth/signup` | 불필요 | 회원가입 |
| POST | `/api/auth/login` | 불필요 | 로그인 → `access_token` 반환 |
| POST | `/api/auth/logout` | 필요 | 로그아웃 |

### 사용자

| Method | Endpoint | 인증 | 설명 |
|--------|----------|------|------|
| GET | `/api/users` | 불필요 | 전체 사용자 목록 |

### 사진

| Method | Endpoint | 인증 | 설명 |
|--------|----------|------|------|
| GET | `/api/photos` | 필요 | 전체 사진 목록 |
| POST | `/api/photos` | 필요 | 사진 업로드 (multipart/form-data) |
| PUT | `/api/photos/{id}` | 필요 (본인) | 설명·키워드 수정 |
| GET | `/api/photos/search?keyword=` | 불필요 | 키워드로 사진 검색 |

### 다이렉트 메시지

| Method | Endpoint | 인증 | 설명 |
|--------|----------|------|------|
| POST | `/api/messages` | 필요 | 메시지 전송 |
| GET | `/api/messages` | 필요 | 수신함 조회 |
| POST | `/api/messages/{id}/reply` | 필요 | 답장 |
| DELETE | `/api/messages/{id}` | 필요 | 메시지 삭제 |