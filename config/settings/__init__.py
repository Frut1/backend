# settings 패키지 초기화 파일

# 환경변수에 따라 적절한 설정 모듈 import
import os

# DJANGO_SETTINGS_MODULE 환경변수 확인
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')

if settings_module == 'config.settings.dev':
    from .dev import *
elif settings_module == 'config.settings.prod':
    from .prod import *
elif settings_module == 'config.settings':
    # 기본값으로 환경 감지
    environment = os.environ.get('DJANGO_ENVIRONMENT', 'dev')
    if environment == 'prod':
        from .prod import *
    else:
        from .dev import *
else:
    # 기본값
    from .dev import *