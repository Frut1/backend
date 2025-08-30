# from config.django.base import SERVER_ENV
import logging
import logging.handlers  # handlers 모듈을 명시적으로 import
import os
import stat
from config.settings import BASE_DIR

# 로그 디렉토리 설정
LOG_DIR = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    # 디렉토리에 setgid 비트 설정 (새로 생성되는 파일이 그룹을 상속받도록)
    os.chmod(LOG_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH | stat.S_ISGID)

# 커스텀 RotatingFileHandler 클래스 정의
class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def _open(self):
        file = super()._open()
        # 파일 권한을 664로 설정 (소유자와 그룹은 읽기/쓰기, 기타는 읽기만)
        try:
            os.chmod(self.baseFilename, 0o664)
        except OSError:
            # 권한 변경 실패 시 무시 (이미 다른 사용자가 소유한 경우)
            pass
        return file
    
    def doRollover(self):
        """롤오버 시에도 권한 설정"""
        super().doRollover()
        # 롤오버된 파일들에 대해서도 권한 설정
        for i in range(self.backupCount, 0, -1):
            sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
            if os.path.exists(sfn):
                try:
                    os.chmod(sfn, 0o664)
                except OSError:
                    pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(levelname)s [PID: %(process)d - %(processName)s] | [TID: %(thread)d - %(threadName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        # "console": {
        #     "level": "DEBUG",
        #     "class": "logging.StreamHandler",
        #     "filters": ["require_debug_true"],
        #     "formatter": "django.server",
        # },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": f"{__name__}.CustomRotatingFileHandler",  # 커스텀 핸들러 사용
            "filename": os.path.join(LOG_DIR, 'app.log'),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "django.server",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# 기존 로그 파일들의 권한 수정 (초기 실행 시)
try:
    log_file = os.path.join(LOG_DIR, 'app.log')
    if os.path.exists(log_file):
        os.chmod(log_file, 0o664)
    
    # 백업 파일들도 권한 수정
    for i in range(1, 6):  # backupCount가 5이므로
        backup_file = f"{log_file}.{i}"
        if os.path.exists(backup_file):
            os.chmod(backup_file, 0o664)
except OSError:
    # 권한 변경 실패 시 무시
    pass

logger = logging.getLogger("django")