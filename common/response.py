from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional


class APIResponse:
    """표준 API 응답 포맷터"""

    @staticmethod
    def success(data: Any = None, message: str = "요청이 성공적으로 처리되었습니다", status_code: int = status.HTTP_200_OK) -> Response:
        """성공 응답 생성"""
        response_data = {
            "success": True,
            "data": data,
            "message": message
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message: str = "요청 처리 중 오류가 발생했습니다", data: Any = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
        """실패 응답 생성"""
        response_data = {
            "success": False,
            "data": data,
            "message": message
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def created(data: Any = None, message: str = "리소스가 성공적으로 생성되었습니다") -> Response:
        """생성 성공 응답"""
        return APIResponse.success(data=data, message=message, status_code=status.HTTP_201_CREATED)

    @staticmethod
    def no_content(message: str = "요청이 성공적으로 처리되었습니다") -> Response:
        """내용 없음 응답"""
        return APIResponse.success(data=None, message=message, status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def not_found(message: str = "요청한 리소스를 찾을 수 없습니다") -> Response:
        """리소스 없음 응답"""
        return APIResponse.error(message=message, status_code=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def unauthorized(message: str = "인증이 필요합니다") -> Response:
        """인증 실패 응답"""
        return APIResponse.error(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message: str = "접근 권한이 없습니다") -> Response:
        """권한 없음 응답"""
        return APIResponse.error(message=message, status_code=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def validation_error(errors: dict, message: str = "입력 데이터가 유효하지 않습니다") -> Response:
        """유효성 검사 실패 응답"""
        return APIResponse.error(message=message, data=errors, status_code=status.HTTP_400_BAD_REQUEST)