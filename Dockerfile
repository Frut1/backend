# Django 프로젝트용 Dockerfile with uv
FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 의존성 파일 복사 및 설치
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# 가상환경을 시스템 PATH에 추가 (핵심!)
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"

# 프로젝트 파일 복사
COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings

# 이제 python 명령어가 가상환경의 python을 사용
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]