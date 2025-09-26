# Frut
# Django Docker Development & Production Setup

이 프로젝트는 Django를 Docker를 사용하여 개발 및 프로덕션 환경에서 실행할 수 있도록 구성되어 있습니다.

## 📋 목차

- [프로젝트 구조](#프로젝트-구조)
- [환경 구성](#환경-구성)
- [빠른 시작](#빠른-시작)
- [개발 환경](#개발-환경)
- [프로덕션 환경](#프로덕션-환경)
- [Make 명령어](#make-명령어)
- [환경변수 설정](#환경변수-설정)
- [GCP Storage 설정](#gcp-storage-설정)
- [데이터베이스 관리](#데이터베이스-관리)
- [SSL/HTTPS 설정](#sslhttps-설정)
- [문제 해결](#문제-해결)

## 📁 프로젝트 구조

```
your-project/
├── docker-compose.dev.yml      # 개발 환경 Docker Compose
├── docker-compose.prod.yml     # 프로덕션 환경 Docker Compose
├── Dockerfile                  # 개발용 Dockerfile
├── Dockerfile.prod             # 프로덕션용 Dockerfile
├── nginx.conf                  # Nginx 설정 파일
├── Makefile                    # 편의 명령어 모음
├── .env.dev                    # 개발용 환경변수
├── .env.prod                   # 프로덕션용 환경변수
├── pyproject.toml              # Python 의존성 (uv 사용)
├── uv.lock                     # 의존성 잠금 파일
└── credentials/
    └── cloud-storage-key.json # GCP 서비스 계정 키
```

## 🏗️ 환경 구성

### 개발 환경 vs 프로덕션 환경

| 구성 요소 | 개발 환경 | 프로덕션 환경 |
|-----------|-----------|---------------|
| **웹 서버** | Django 개발 서버 | Gunicorn + Nginx |
| **포트 노출** | 직접 노출 (8000, 3306, 6378) | Nginx만 노출 (80, 443) |
| **코드 반영** | 실시간 (볼륨 마운트) | 이미지 빌드 시점 |
| **정적 파일** | Django 서빙 | Nginx 서빙 |
| **SSL** | 미사용 | 지원 |
| **디버그 모드** | 활성화 | 비활성화 |

## 🚀 빠른 시작

### 1. 저장소 클론 및 환경 설정

```bash
git clone <repository-url>
cd <project-name>

# 환경변수 파일 복사 및 수정
cp .env.dev.example .env.dev
cp .env.prod.example .env.prod

# 환경변수 파일 편집
nano .env.dev
nano .env.prod
```

### 2. GCP 서비스 계정 키 설정

```bash
mkdir -p credentials
# GCP에서 다운로드한 서비스 계정 키를 credentials/ 폴더에 복사
cp path/to/your/service-account-key.json credentials/
```

### 3. 개발 환경 실행

```bash
make dev
```

## 🛠️ 개발 환경

### 시작하기

```bash
# 개발 환경 시작
make dev

# 또는 빌드 후 시작
make dev-build
```

### 개발 환경 특징

- **실시간 코드 반영**: 코드 변경 시 자동으로 서버 재시작
- **포트 직접 접근**: 
  - Django: http://localhost:8000
  - MySQL: localhost:3306
  - Redis: localhost:6378
- **디버그 모드**: 활성화되어 상세한 에러 메시지 표시
- **CORS**: 모든 오리진 허용

### 개발 중 자주 사용하는 명령어

```bash
# Django 쉘 접속
make shell

# 마이그레이션 생성
make makemigrations

# 마이그레이션 실행
make migrate

# 슈퍼유저 생성
make createsuperuser

# 테스트 실행
make test

# 로그 확인
make logs
```

## 🏭 프로덕션 환경

### 배포하기

```bash
# 프로덕션 환경 빌드 및 시작
make prod-build

# 정적 파일 수집
make collectstatic

# 마이그레이션 실행
make migrate-prod
```

### 프로덕션 환경 특징

- **고성능**: Gunicorn + Nginx 조합
- **보안**: 내부 네트워크 통신, HTTPS 지원
- **정적 파일**: Nginx가 직접 서빙하여 성능 최적화
- **로드 밸런싱**: Gunicorn workers로 부하 분산
- **캐싱**: Nginx의 정적 파일 캐싱

### 프로덕션 모니터링

```bash
# 프로덕션 로그 확인
make logs-prod

# Nginx 로그 확인
make logs-nginx

# 컨테이너 상태 확인
docker compose -f docker-compose.prod.yml ps
```

## 📜 Make 명령어

### 환경 관리

```bash
make dev             # 개발 환경 시작
make prod            # 프로덕션 환경 시작
make dev-build       # 개발 환경 빌드 후 시작
make prod-build      # 프로덕션 환경 빌드 후 시작
make dev-down        # 개발 환경 중지
make prod-down       # 프로덕션 환경 중지
make restart         # 개발 환경 재시작
make restart-prod    # 프로덕션 환경 재시작
```

### Django 관리

```bash
# 개발 환경 명령어
make shell           # Django 쉘
make migrate         # 마이그레이션 실행
make makemigrations  # 마이그레이션 생성
make createsuperuser # 슈퍼유저 생성
make test            # 테스트 실행

# 프로덕션 환경 명령어 (-prod 접미사)
make shell-prod
make migrate-prod
make createsuperuser-prod
make collectstatic   # 정적 파일 수집
```

### 로그 및 모니터링

```bash
make logs            # 개발 환경 Django 로그
make logs-prod       # 프로덕션 환경 Django 로그
make logs-nginx      # Nginx 로그
```

### 데이터베이스

```bash
make mysql-shell     # MySQL 쉘 접속 (개발)
make mysql-shell-prod # MySQL 쉘 접속 (프로덕션)
```

### 도움말

```bash
make help            # 사용 가능한 모든 명령어 보기
```

## ⚙️ 환경변수 설정

### 개발 환경 (.env.dev)

```bash
# Django 설정
DEBUG=True
SECRET_KEY=your-dev-secret-key
DJANGO_SETTINGS_MODULE=config.settings.dev

# 데이터베이스
DB_NAME=erp_dev
DB_USER=kingbus
DB_PASSWORD=dev_password
DB_HOST=mysql_service
DB_PORT=3306

# MySQL 컨테이너 설정
MYSQL_ROOT_PASSWORD=root_password_dev
MYSQL_DATABASE=erp_dev
MYSQL_USER=kingbus
MYSQL_PASSWORD=dev_password

# Redis
REDIS_URL=redis://redis_service:6379/0

# GCP Storage
GCS_BUCKET_NAME=frut-storage-dev
GCS_PROJECT_ID=your-project-id
GCS_CREDENTIALS_PATH=/app/credentials/service-account-key.json

# CORS
CORS_ALLOW_ALL_ORIGINS=True
```

### 프로덕션 환경 (.env.prod)

```bash
# Django 설정
DEBUG=False
SECRET_KEY=your-super-strong-production-secret-key
DJANGO_SETTINGS_MODULE=config.settings.prod
ALLOWED_HOSTS=your-domain.com,server-ip

# 데이터베이스 (강력한 패스워드 사용)
DB_NAME=erp_prod
DB_USER=kingbus
DB_PASSWORD=strong_production_password
DB_HOST=mysql_service
DB_PORT=3306

# 보안 설정
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# GCP Storage
GCS_BUCKET_NAME=frut-storage-prod
GCS_FILE_OVERWRITE=False

# CORS (특정 도메인만 허용)
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

## ☁️ GCP Storage 설정

### 1. GCP 프로젝트 설정

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. Cloud Storage API 활성화

### 2. Storage 버킷 생성

```bash
# gcloud CLI 사용 (선택사항)
gsutil mb gs://frut-storage-dev
gsutil mb gs://frut-storage-prod
```

### 3. 서비스 계정 생성

1. IAM 및 관리 → 서비스 계정
2. 새 서비스 계정 생성
3. 역할 추가:
   - `Storage Object Admin`
   - `Storage Legacy Bucket Reader`
4. JSON 키 다운로드
5. `credentials/service-account-key.json`에 저장

### 4. Django 설정

```python
# settings/base.py
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')
GS_PROJECT_ID = os.environ.get('GCS_PROJECT_ID')
```

## 🗄️ 데이터베이스 관리

### 마이그레이션

```bash
# 마이그레이션 생성
make makemigrations

# 특정 앱 마이그레이션
make makemigrations users accounts

# 마이그레이션 실행
make migrate

# 마이그레이션 상태 확인
make showmigrations
```

### 데이터베이스 백업 및 복원

```bash
# 개발 데이터베이스 백업
docker compose -f docker-compose.dev.yml exec mysql_service \
  mysqldump -u kingbus -p erp_dev > backup_dev.sql

# 프로덕션 데이터베이스 백업
docker compose -f docker-compose.prod.yml exec mysql_service \
  mysqldump -u kingbus -p erp_prod > backup_prod.sql

# 백업 복원
docker compose -f docker-compose.dev.yml exec -T mysql_service \
  mysql -u kingbus -p erp_dev < backup_dev.sql
```

## 🔒 SSL/HTTPS 설정

### 1. Let's Encrypt 인증서 발급

```bash
# 서버에서 실행
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# 인증서 파일을 ssl/ 폴더에 복사
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

### 2. nginx.conf 수정

```nginx
# nginx.conf에서 HTTPS 섹션 주석 해제
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... 나머지 설정
}
```

### 3. 자동 갱신 설정

```bash
# crontab 편집
sudo crontab -e

# 다음 라인 추가 (매월 1일 새벽 2시에 갱신)
0 2 1 * * certbot renew --quiet && docker compose -f docker-compose.prod.yml restart nginx
```

## 🔧 문제 해결

### 자주 발생하는 문제들

#### 1. 포트 충돌

```bash
# 사용 중인 포트 확인
sudo netstat -tulpn | grep :8000

# 프로세스 종료
sudo kill -9 <PID>
```

#### 2. 권한 문제

```bash
# Docker 권한 추가
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. 볼륨 권한 문제

```bash
# 볼륨 삭제 후 재생성
docker volume rm $(docker volume ls -q)
make dev-build
```

#### 4. MySQL 연결 오류

```bash
# MySQL 컨테이너 로그 확인
make logs
docker compose -f docker-compose.dev.yml logs mysql_service

# MySQL 컨테이너 재시작
docker compose -f docker-compose.dev.yml restart mysql_service
```

#### 5. 정적 파일 문제 (프로덕션)

```bash
# 정적 파일 재수집
make collectstatic

# Nginx 설정 테스트
docker compose -f docker-compose.prod.yml exec nginx nginx -t

# Nginx 재시작
docker compose -f docker-compose.prod.yml restart nginx
```

### 로그 확인

```bash
# 모든 서비스 로그
docker compose -f docker-compose.dev.yml logs

# 특정 서비스 로그
docker compose -f docker-compose.dev.yml logs web
docker compose -f docker-compose.prod.yml logs nginx

# 실시간 로그 추적
make logs
```

### 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker compose -f docker-compose.dev.yml ps

# 컨테이너 리소스 사용량
docker stats

# 컨테이너 내부 접속
docker compose -f docker-compose.dev.yml exec web bash
```

## 📝 추가 참고사항

### 보안 체크리스트

- [ ] `.env.prod` 파일을 Git에서 제외 (.gitignore)
- [ ] 강력한 SECRET_KEY 설정
- [ ] 데이터베이스 패스워드 변경
- [ ] ALLOWED_HOSTS 적절히 설정
- [ ] SSL 인증서 설정
- [ ] 방화벽 설정 (필요한 포트만 개방)

### 성능 최적화

- [ ] Gunicorn workers 수 조정
- [ ] Nginx 캐싱 설정
- [ ] 데이터베이스 인덱스 최적화
- [ ] 정적 파일 CDN 사용 고려

### 모니터링

- [ ] 로그 수집 시스템 구축
- [ ] 헬스 체크 엔드포인트 설정
- [ ] 메트릭 수집 (Prometheus + Grafana)
- [ ] 알림 시스템 구축

---

🎉 **Happy Coding!** 

문제가 발생하면 로그를 확인하고, GitHub Issues에 문의해주세요.