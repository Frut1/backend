.PHONY: up down build logs shell migrate makemigrations createsuperuser

# Docker Compose 기본 명령어들
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up --build -d

logs:
	docker-compose logs -f web

# Django 관리 명령어들
shell:
	docker-compose exec web python manage.py shell

# 사용법: make migrate [app1 app2 ...]
migrate:
	docker-compose exec web python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

# 사용법: make makemigrations [app1 app2 ...]  
makemigrations:
	docker-compose exec web python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

# 모든 로컬 앱의 마이그레이션 자동 생성 (쉘 스크립트 방식)
makemigrations-all:
	docker-compose exec web bash /app/makemigrations_all.sh

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# 앱 이름들을 타겟으로 인식하지 않도록 설정
%:
	@:

# 데이터베이스 관리
mysql-shell:
	docker-compose exec mysql_service mysql -u kingbus -p erp

# 개발 도구
# 개발 도구
test:
	docker-compose exec web python manage.py test $(filter-out $@,$(MAKECMDGOALS))

# 마이그레이션 관련 유틸리티
showmigrations:
	docker-compose exec web python manage.py showmigrations $(filter-out $@,$(MAKECMDGOALS))

# 마이그레이션 상태 확인
migrate-check:
	docker-compose exec web python manage.py migrate --check

# 특정 마이그레이션으로 롤백 (사용법: make migrate-to users 0001)
migrate-to:
	docker-compose exec web python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

# 전체 재시작
restart:
	docker-compose down
	docker-compose up --build -d