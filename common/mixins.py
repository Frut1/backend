from rest_framework import status
from rest_framework.response import Response
from .response import APIResponse


class StandardResponseMixin:
    """DRF View에서 표준 응답 형식을 사용하기 위한 믹스인"""

    def create(self, request, *args, **kwargs):
        """POST 요청 처리 - 생성"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return APIResponse.created(
                data=self.get_serializer(instance).data,
                message="리소스가 성공적으로 생성되었습니다"
            )
        return APIResponse.validation_error(serializer.errors)

    def list(self, request, *args, **kwargs):
        """GET 요청 처리 - 목록"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # 페이지네이션 응답을 표준 형식으로 래핑
            return APIResponse.success(
                data=paginated_response.data,
                message="목록을 성공적으로 조회했습니다"
            )

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="목록을 성공적으로 조회했습니다"
        )

    def retrieve(self, request, *args, **kwargs):
        """GET 요청 처리 - 상세"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse.success(
                data=serializer.data,
                message="상세 정보를 성공적으로 조회했습니다"
            )
        except:
            return APIResponse.not_found()

    def update(self, request, *args, **kwargs):
        """PUT/PATCH 요청 처리 - 수정"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            if serializer.is_valid():
                serializer.save()
                return APIResponse.success(
                    data=serializer.data,
                    message="리소스가 성공적으로 수정되었습니다"
                )
            return APIResponse.validation_error(serializer.errors)
        except:
            return APIResponse.not_found()

    def destroy(self, request, *args, **kwargs):
        """DELETE 요청 처리 - 삭제"""
        try:
            instance = self.get_object()
            instance.delete()
            return APIResponse.no_content(message="리소스가 성공적으로 삭제되었습니다")
        except:
            return APIResponse.not_found()


class StandardAPIViewMixin:
    """APIView에서 표준 응답 형식을 사용하기 위한 믹스인"""

    def handle_exception(self, exc):
        """예외 처리를 표준 응답 형식으로 변환"""
        response = super().handle_exception(exc)

        if hasattr(response, 'status_code'):
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                return APIResponse.validation_error(
                    errors=response.data if hasattr(response, 'data') else {},
                    message="입력 데이터가 유효하지 않습니다"
                )
            elif response.status_code == status.HTTP_401_UNAUTHORIZED:
                return APIResponse.unauthorized()
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                return APIResponse.forbidden()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                return APIResponse.not_found()

        return response