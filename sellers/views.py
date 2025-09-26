from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db.models import Exists, OuterRef

from common.response import APIResponse
from common.mixins import StandardAPIViewMixin
from users.models import User, UserTypeChoices
from .models import FarmProfile, FarmFollow
from .serializers import FarmListSerializer, FarmFollowSerializer


class FarmListPagination(PageNumberPagination):
    """농장 목록 페이지네이션"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class FarmListView(StandardAPIViewMixin, APIView):
    """활성화된 농장 목록 조회 API"""
    permission_classes = [IsAuthenticated]
    pagination_class = FarmListPagination

    @extend_schema(
        operation_id="farm_list",
        summary="농장 목록 조회",
        description="활성화된 농장들의 목록을 조회합니다. 각 농장의 팔로우 여부도 함께 반환합니다.",
        responses={
            200: OpenApiResponse(description="농장 목록 조회 성공"),
            401: OpenApiResponse(description="인증 실패"),
        }
    )
    def get(self, request):
        # 활성화된 판매자 유저들의 농장 프로필 조회
        queryset = FarmProfile.objects.select_related('user').filter(
            user__user_type=UserTypeChoices.SELLER,
            user__is_active=True,
            farm_name__isnull=False  # 농장명이 있는 경우만
        ).exclude(
            farm_name=''  # 빈 문자열 제외
        ).order_by('-created_at')

        # 페이지네이션 적용
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = FarmListSerializer(
                page,
                many=True,
                context={'request': request}
            )
            paginated_response = paginator.get_paginated_response(serializer.data)

            return APIResponse.success(
                data=paginated_response.data,
                message="농장 목록을 성공적으로 조회했습니다."
            )

        # 페이지네이션이 적용되지 않은 경우
        serializer = FarmListSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return APIResponse.success(
            data={'results': serializer.data},
            message="농장 목록을 성공적으로 조회했습니다."
        )


class FarmFollowView(StandardAPIViewMixin, APIView):
    """농장 팔로우/언팔로우 API"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="farm_follow_toggle",
        summary="농장 팔로우/언팔로우",
        description="지정된 농장에 대한 팔로우 상태를 토글합니다. 팔로우 중이면 언팔로우, 아니면 팔로우합니다.",
        request=FarmFollowSerializer,
        responses={
            200: OpenApiResponse(description="팔로우 상태 변경 성공"),
            400: OpenApiResponse(description="유효성 검사 실패"),
            401: OpenApiResponse(description="인증 실패"),
            404: OpenApiResponse(description="농장을 찾을 수 없음"),
        }
    )
    def post(self, request, farm_id):
        # URL에서 farm_id를 가져와서 serializer에 전달
        data = {'farm_id': farm_id}
        serializer = FarmFollowSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                result = serializer.save()
                return APIResponse.success(
                    data={
                        'is_following': result['is_following'],
                        'follower_count': result['follower_count']
                    },
                    message=result['message']
                )

            except Exception as e:
                return APIResponse.error(
                    message="팔로우 처리 중 오류가 발생했습니다.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="유효하지 않은 요청입니다."
        )
