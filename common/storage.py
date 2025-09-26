"""
GCP Cloud Storage 유틸리티 모듈
다른 앱에서 공통으로 사용할 수 있는 GCS 관련 함수들
"""
import os
import uuid
from datetime import datetime
from typing import Optional, Tuple
from django.conf import settings
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
import logging

logger = logging.getLogger(__name__)


def get_gcs_client():
    """GCS 클라이언트 인스턴스 반환"""
    try:
        if settings.GCS_CREDENTIALS_PATH and os.path.exists(settings.GCS_CREDENTIALS_PATH):
            client = storage.Client.from_service_account_json(
                settings.GCS_CREDENTIALS_PATH,
                project=settings.GCS_PROJECT_ID
            )
        else:
            # 환경에서 자동으로 인증 정보를 가져옴 (서버 환경)
            client = storage.Client(project=settings.GCS_PROJECT_ID)
        return client
    except Exception as e:
        logger.error(f"GCS 클라이언트 생성 실패: {e}")
        raise


def upload_file_to_gcs(file, folder_path: str, filename: Optional[str] = None) -> Tuple[bool, str]:
    """
    파일을 GCS에 업로드

    Args:
        file: Django UploadedFile 객체
        folder_path: GCS 내 폴더 경로 (예: 'farms/profiles')
        filename: 사용할 파일명 (None이면 자동 생성)

    Returns:
        Tuple[bool, str]: (성공여부, URL 또는 에러메시지)
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(settings.GCS_BUCKET_NAME)

        # 파일명 생성
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = os.path.splitext(file.name)[1]
            filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

        # GCS 경로 생성
        blob_name = f"{folder_path.rstrip('/')}/{filename}"
        blob = bucket.blob(blob_name)

        # 파일 업로드
        file.seek(0)  # 파일 포인터를 처음으로 이동
        blob.upload_from_file(
            file,
            content_type=file.content_type,
            predefined_acl=settings.GCS_DEFAULT_ACL
        )

        # 공개 URL 반환
        if settings.GCS_DEFAULT_ACL == 'publicRead':
            url = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/{blob_name}"
        else:
            url = blob.generate_signed_url(expiration=3600)  # 1시간 임시 URL

        logger.info(f"파일 업로드 성공: {blob_name}")
        return True, url

    except GoogleCloudError as e:
        logger.error(f"GCS 업로드 실패: {e}")
        return False, f"파일 업로드 실패: {str(e)}"
    except Exception as e:
        logger.error(f"파일 업로드 중 오류: {e}")
        return False, f"파일 업로드 중 오류: {str(e)}"


def delete_file_from_gcs(file_url: str) -> bool:
    """
    GCS에서 파일 삭제

    Args:
        file_url: 삭제할 파일의 URL

    Returns:
        bool: 삭제 성공 여부
    """
    try:
        if not file_url.startswith(f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}"):
            logger.warning(f"유효하지 않은 GCS URL: {file_url}")
            return False

        # URL에서 blob 이름 추출
        blob_name = file_url.replace(f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/", "")

        client = get_gcs_client()
        bucket = client.bucket(settings.GCS_BUCKET_NAME)
        blob = bucket.blob(blob_name)

        blob.delete()
        logger.info(f"파일 삭제 성공: {blob_name}")
        return True

    except GoogleCloudError as e:
        logger.error(f"GCS 파일 삭제 실패: {e}")
        return False
    except Exception as e:
        logger.error(f"파일 삭제 중 오류: {e}")
        return False


def get_file_url(blob_name: str, signed: bool = False) -> str:
    """
    GCS 파일 URL 생성

    Args:
        blob_name: GCS 내 파일 경로
        signed: 서명된 URL 생성 여부

    Returns:
        str: 파일 URL
    """
    try:
        if signed:
            client = get_gcs_client()
            bucket = client.bucket(settings.GCS_BUCKET_NAME)
            blob = bucket.blob(blob_name)
            return blob.generate_signed_url(expiration=3600)
        else:
            return f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/{blob_name}"

    except Exception as e:
        logger.error(f"URL 생성 실패: {e}")
        return ""


def validate_file(file, max_size_mb: int = 5, allowed_extensions: list = None) -> Tuple[bool, str]:
    """
    파일 유효성 검사

    Args:
        file: Django UploadedFile 객체
        max_size_mb: 최대 파일 크기 (MB)
        allowed_extensions: 허용 확장자 리스트

    Returns:
        Tuple[bool, str]: (유효여부, 에러메시지)
    """
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']

    # 파일 크기 검사
    if file.size > max_size_mb * 1024 * 1024:
        return False, f"파일 크기는 {max_size_mb}MB를 초과할 수 없습니다."

    # 확장자 검사
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        return False, f"허용되지 않는 파일 형식입니다. 허용 형식: {', '.join(allowed_extensions)}"

    return True, ""