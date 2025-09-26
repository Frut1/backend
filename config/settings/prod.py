from .base import *
import environ

# 프로덕션용 .env 파일 읽기
environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))

# 프로덕션 환경 설정
DEBUG = False

# 프로덕션용 ALLOWED_HOSTS (보안 강화)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])
APPEND_SLASH = True

# Redis 설정 (프로덕션용)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://redis_service:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            }
        },
        'TIMEOUT': 60 * 60 * 24 * 7,
    }
}

# 보안 설정
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1년

# HTTPS 설정 (SSL 사용시)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)

# 프록시 설정 (Nginx 뒤에서 실행)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# CORS 설정 (프로덕션용 - 특정 도메인만 허용)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True

# 정적 파일 설정 (프로덕션용)
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static/'

# 미디어 파일 설정 (프로덕션용)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# GCP Storage 설정 (프로덕션용)
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# GCS 설정
GS_BUCKET_NAME = GCS_BUCKET_NAME
GS_PROJECT_ID = GCS_PROJECT_ID
GS_CREDENTIALS = GCS_CREDENTIALS_PATH
GS_DEFAULT_ACL = GCS_DEFAULT_ACL
GS_FILE_OVERWRITE = GCS_FILE_OVERWRITE
GS_CUSTOM_ENDPOINT = f'https://storage.googleapis.com/{GCS_BUCKET_NAME}'

# 미디어 파일 URL 설정
MEDIA_URL = f'https://storage.googleapis.com/{GCS_BUCKET_NAME}/'

# 프로덕션용 로깅 (에러 중심)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/app/log/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# # 프로덕션용 이메일 설정
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = env('EMAIL_PORT', default=587)
# EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
# EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# 관리자 설정
ADMINS = [
    ('Admin', env('ADMIN_EMAIL', default='admin@example.com')),
]

# 성능 최적화
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 데이터베이스 연결 풀링 (선택사항)
DATABASES['default']['CONN_MAX_AGE'] = 60

print("🚀 Production settings loaded")