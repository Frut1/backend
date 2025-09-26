from .base import *
import environ

# 개발용 .env 파일 읽기
environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))

# 개발 환경 설정
DEBUG = True

# 개발용 ALLOWED_HOSTS (더 관대함)
ALLOWED_HOSTS = ['*']
APPEND_SLASH = False

# 개발용 미들웨어 (debug toolbar 추가)
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar 추가
] + MIDDLEWARE

# 개발용 앱 (debug toolbar 추가)
INSTALLED_APPS += [
    'debug_toolbar',
]

# Redis 설정 (개발용 - localhost)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://redis_service:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 60 * 60 * 24 * 7,  # 기본 만료 시간 7일
    }
}

# Debug Toolbar 설정
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",  # Docker 환경
]

# 개발용 CORS 설정 (모든 오리진 허용)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 개발용 로깅 (더 상세한 로그)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            # 'level': 'DEBUG',  # SQL 쿼리 로그
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# 개발용 이메일 백엔드 (콘솔 출력)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 개발용 GCP Storage (선택적으로 로컬 파일 시스템 사용 가능)
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'  # 로컬 파일 시스템 사용하려면 주석 해제

print("🔧 Development settings loaded")