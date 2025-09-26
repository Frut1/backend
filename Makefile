.PHONY: dev prod dev-build prod-build down logs shell migrate makemigrations createsuperuser test

# 환경별 Docker Compose 실행
dev:
	docker compose -f docker-compose.dev.yml up -d

prod:
	docker compose -f docker-compose.prod.yml up -d

dev-build:
	docker compose -f docker-compose.dev.yml up --build -d

prod-build:
	docker compose -f docker-compose.prod.yml up --build -d

# 환경별 종료
dev-down:
	docker compose -f docker-compose.dev.yml down

prod-down:
	docker compose -f docker-compose.prod.yml down

down:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.prod.yml down

# 로그 확인 (기본은 개발환경)
logs:
	docker compose -f docker-compose.dev.yml logs -f web

logs-prod:
	docker compose -f docker-compose.prod.yml logs -f web

logs-nginx:
	docker compose -f docker-compose.prod.yml logs -f nginx

# Django 관리 명령어들 (개발환경 기준)
shell:
	docker compose -f docker-compose.dev.yml exec web python manage.py shell

shell-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py shell

# 마이그레이션 (사용법: make migrate [app1 app2 ...])
migrate:
	docker compose -f docker-compose.dev.yml exec web python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

migrate-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

# 마이그레이션 생성 (사용법: make makemigrations [app1 app2 ...])
makemigrations:
	docker compose -f docker-compose.dev.yml exec web python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

makemigrations-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

# 모든 로컬 앱의 마이그레이션 자동 생성
makemigrations-all:
	docker compose -f docker-compose.dev.yml exec web bash /app/makemigrations_all.sh

makemigrations-all-prod:
	docker compose -f docker-compose.prod.yml exec web bash /app/makemigrations_all.sh

# 슈퍼유저 생성
createsuperuser:
	docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

createsuperuser-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# 마이그레이션 파일 삭제
clear-migrations:
	docker compose -f docker-compose.dev.yml exec web find . -type d -name "migrations" -not -path "./.venv/*" -exec find {} -type f -name "*.py" -not -name "__init__.py" -delete \;

# 앱 이름들을 타겟으로 인식하지 않도록 설정
%:
	@:

# 데이터베이스 쉘 접속
mysql-shell:
	docker compose -f docker-compose.dev.yml exec mysql_service mysql -u kingbus -p erp

mysql-shell-prod:
	docker compose -f docker-compose.prod.yml exec mysql_service mysql -u kingbus -p erp

# 개발 도구
test:
	docker compose -f docker-compose.dev.yml exec web python manage.py test $(filter-out $@,$(MAKECMDGOALS))

test-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py test $(filter-out $@,$(MAKECMDGOALS))

# 마이그레이션 관련 유틸리티
showmigrations:
	docker compose -f docker-compose.dev.yml exec web python manage.py showmigrations $(filter-out $@,$(MAKECMDGOALS))

showmigrations-prod:
	docker compose -f docker-compose.prod.yml exec web python manage.py showmigrations $(filter-out $@,$(MAKECMDGOALS))


migrate-check:
	docker compose -f docker-compose.dev.yml exec web python manage.py migrate --check

# 특정 마이그레이션으로 롤백 (사용법: make migrate-to users 0001)
migrate-to:
	docker compose -f docker-compose.dev.yml exec web python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

# 전체 재시작
restart:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.dev.yml up --build -d

restart-prod:
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.prod.yml up --build -d

# 정적 파일 수집 (프로덕션용)
collectstatic:
	docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 헬프 메시지
help:
	@echo "Available commands:"
	@echo "  dev              - Start development environment"
	@echo "  prod             - Start production environment"
	@echo "  dev-build        - Build and start development environment"
	@echo "  prod-build       - Build and start production environment"
	@echo "  dev-down         - Stop development environment"
	@echo "  prod-down        - Stop production environment"
	@echo "  logs             - Show development logs"
	@echo "  logs-prod        - Show production logs"
	@echo "  logs-nginx       - Show nginx logs"
	@echo "  shell            - Access Django shell (dev)"
	@echo "  migrate          - Run migrations (dev)"
	@echo "  makemigrations   - Create migrations (dev)"
	@echo "  createsuperuser  - Create superuser (dev)"
	@echo "  test             - Run tests (dev)"
	@echo "  collectstatic    - Collect static files (prod)"