# MBFI

금융 성향 테스트 & AI 기반 개인화 금융 분석 서비스입니다.

## 디렉터리 구조

```text
MBFI/
├─ frontend/       # Vue 3 + TypeScript + Vite
├─ backend/        # Java 21 + Spring Boot
├─ ai/             # Python 3.12 + FastAPI
├─ docker-compose.yml
└─ .env.example
```

환경별 설정은 Backend의 `application.yml`, `application-local.yml`, `application-prod.yml`과 Frontend의 `.env.example`로 분리했습니다. 

## 의존성

- Frontend: Vue 3, Vue Router, Pinia, Tailwind CSS, Vite, TypeScript
- Backend: Spring Boot Web, Validation, Data JPA, PostgreSQL driver, JUnit
- AI: FastAPI, Uvicorn, Pydantic, HTTPX, Pytest
- Infrastructure: PostgreSQL 16 Docker image

## 실행

```powershell
Copy-Item .env.example .env
docker compose up -d postgres

cd frontend
npm install
npm run dev
```

Frontend 환경변수는 `frontend/.env.example`을 복사해 설정할 수 있습니다. 실제 API 호출은 Spring Boot를 통해서만 이루어집니다.

별도 터미널에서 Backend는 `backend` 디렉터리에서 `gradle bootRun`으로 실행합니다. Gradle이 설치되어 있지 않다면 Gradle Wrapper를 생성하거나 IDE의 Gradle 실행 기능을 사용하세요.

AI 서버:

```powershell
cd ai
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 엔드포인트

- Backend: `GET http://localhost:8080/health`
- Backend → AI 예제: `GET http://localhost:8080/api/internal/ai/health`
- AI: `GET http://localhost:8000/health`
- Frontend: `http://localhost:5173`

Backend가 점수와 성향 유형을 결정하고, AI 서버는 전달받은 결과를 설명하는 역할만 담당하도록 경계를 유지합니다. 현재 리포트 엔드포인트는 의도적으로 placeholder입니다.

## 환경변수

`.env.example`을 복사해 로컬 값을 설정하세요. 비밀번호, API Key 등 민감정보는 `.env`에만 두며 Git에 커밋하지 않습니다. 외부 LLM API Key는 현재 사용하지 않습니다.

## 검증

```powershell
cd frontend; npm run build
cd ../ai; pytest
cd ../backend; gradle test
docker compose config
```

실행 환경에 따라 전역 `gradle`, Python, Docker Desktop 설치 여부가 다를 수 있습니다. 검증 결과는 작업 완료 보고에 실제 실행 결과로 기록합니다.

## 후속 구현

금융 문항/점수 도메인과 결과 저장, AI 요청 DTO 및 내부 인증, 비동기 리포트 생성, PDF/이메일, 결제/주문/상품 도메인, 관찰성·Rate Limit·운영용 보안 설정이 남아 있습니다.
