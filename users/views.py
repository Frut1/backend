from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.response import APIResponse
from common.mixins import StandardAPIViewMixin
from .models import User, UserTypeChoices
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    LogoutSerializer,
    UserWithdrawalSerializer,
    PasswordChangeSerializer,
    AdminUserListSerializer
)


class RegisterView(StandardAPIViewMixin, APIView):
    """회원가입 API"""
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="user_register",
        summary="회원가입",
        description="새로운 사용자 계정을 생성합니다.",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(description="회원가입 성공"),
            400: OpenApiResponse(description="유효성 검사 실패"),
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data

            return APIResponse.created(
                data=user_data,
                message="회원가입이 성공적으로 완료되었습니다."
            )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="회원가입 정보가 유효하지 않습니다."
        )


class LoginView(StandardAPIViewMixin, APIView):
    """로그인 API"""
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="user_login",
        summary="로그인",
        description="아이디와 비밀번호로 로그인하고 JWT 토큰을 발급받습니다.",
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(description="로그인 성공"),
            400: OpenApiResponse(description="로그인 실패"),
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # 사용자 정보와 토큰 반환
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                }
            }

            return APIResponse.success(
                data=response_data,
                message="로그인이 성공적으로 완료되었습니다."
            )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="로그인 정보가 올바르지 않습니다."
        )


class LogoutView(StandardAPIViewMixin, APIView):
    """로그아웃 API"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="user_logout",
        summary="로그아웃",
        description="리프레시 토큰을 무효화하여 로그아웃합니다.",
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(description="로그아웃 성공"),
            400: OpenApiResponse(description="유효하지 않은 토큰"),
        }
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return APIResponse.success(
                    message="로그아웃이 성공적으로 완료되었습니다."
                )
            except Exception:
                return APIResponse.error(
                    message="로그아웃 처리 중 오류가 발생했습니다.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="유효하지 않은 토큰입니다."
        )


class CustomTokenRefreshView(StandardAPIViewMixin, TokenRefreshView):
    """토큰 재발급 API - SimpleJWT의 TokenRefreshView를 커스터마이징"""

    @extend_schema(
        operation_id="token_refresh",
        summary="토큰 재발급",
        description="리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받습니다.",
        responses={
            200: OpenApiResponse(description="토큰 재발급 성공"),
            401: OpenApiResponse(description="유효하지 않은 리프레시 토큰"),
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            return APIResponse.success(
                data=response.data,
                message="토큰이 성공적으로 재발급되었습니다."
            )
        else:
            return APIResponse.unauthorized(
                message="유효하지 않은 리프레시 토큰입니다."
            )


class WithdrawView(StandardAPIViewMixin, APIView):
    """회원 탈퇴 API"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="user_withdraw",
        summary="회원 탈퇴",
        description="현재 로그인한 사용자의 계정을 탈퇴 처리합니다.",
        request=UserWithdrawalSerializer,
        responses={
            200: OpenApiResponse(description="탈퇴 처리 성공"),
            400: OpenApiResponse(description="유효성 검사 실패"),
            401: OpenApiResponse(description="인증 실패"),
        }
    )
    def post(self, request):
        serializer = UserWithdrawalSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                # 사용자 탈퇴 처리
                user = serializer.save()

                # 현재 사용자의 모든 리프레시 토큰 무효화
                try:
                    from rest_framework_simplejwt.tokens import RefreshToken
                    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

                    # 사용자의 모든 outstanding token을 블랙리스트에 추가
                    tokens = OutstandingToken.objects.filter(user=user)
                    for outstanding_token in tokens:
                        try:
                            token = RefreshToken(outstanding_token.token)
                            token.blacklist()
                        except Exception:
                            pass  # 이미 만료되었거나 무효한 토큰은 무시
                except Exception:
                    # 토큰 블랙리스트 처리 실패는 무시 (탈퇴는 이미 완료됨)
                    pass

                return APIResponse.success(
                    message="회원 탈퇴가 성공적으로 처리되었습니다."
                )

            except Exception as e:
                return APIResponse.error(
                    message="탈퇴 처리 중 오류가 발생했습니다.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="탈퇴 정보가 유효하지 않습니다."
        )


class PasswordChangeView(StandardAPIViewMixin, APIView):
    """비밀번호 변경 API"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="user_change_password",
        summary="비밀번호 변경",
        description="현재 비밀번호를 확인하고 새로운 비밀번호로 변경합니다.",
        request=PasswordChangeSerializer,
        responses={
            200: OpenApiResponse(description="비밀번호 변경 성공"),
            400: OpenApiResponse(description="유효성 검사 실패"),
            401: OpenApiResponse(description="인증 실패"),
        }
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                # 비밀번호 변경 처리
                serializer.save()

                return APIResponse.success(
                    message="비밀번호가 성공적으로 변경되었습니다."
                )

            except Exception as e:
                return APIResponse.error(
                    message="비밀번호 변경 중 오류가 발생했습니다.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return APIResponse.validation_error(
            errors=serializer.errors,
            message="비밀번호 변경 정보가 유효하지 않습니다."
        )


class AdminUserListPagination(PageNumberPagination):
    """관리자 유저 목록 페이지네이션"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminUserListView(StandardAPIViewMixin, APIView):
    """관리자 페이지용 유저 목록 조회 API"""
    permission_classes = [IsAuthenticated]
    pagination_class = AdminUserListPagination

    def check_admin_permission(self, request):
        """관리자 권한 확인"""
        if not request.user.is_authenticated or request.user.user_type != UserTypeChoices.ADMIN:
            return False
        return True

    @extend_schema(
        operation_id="admin_user_list",
        summary="관리자용 유저 목록 조회",
        description="관리자가 플랫폼의 모든 유저 목록을 조회합니다. (ADMIN 타입 제외)",
        responses={
            200: OpenApiResponse(description="유저 목록 조회 성공"),
            401: OpenApiResponse(description="인증 실패"),
            403: OpenApiResponse(description="관리자 권한 필요"),
        }
    )
    def get(self, request):
        # 관리자 권한 확인
        if not self.check_admin_permission(request):
            return APIResponse.forbidden(
                message="관리자 권한이 필요합니다."
            )

        # ADMIN 타입 제외한 모든 유저 조회
        queryset = User.objects.select_related('farmprofile').exclude(
            user_type=UserTypeChoices.ADMIN
        ).order_by('-date_joined')

        # 검색 기능
        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        # 필터링
        user_type = request.GET.get('user_type')
        if user_type and user_type in [choice[0] for choice in UserTypeChoices.choices if choice[0] != UserTypeChoices.ADMIN]:
            queryset = queryset.filter(user_type=user_type)

        status_filter = request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 정렬
        ordering = request.GET.get('ordering', '-date_joined')
        if ordering in ['-date_joined', 'date_joined', 'name', '-name']:
            queryset = queryset.order_by(ordering)

        # 전체 유저 수 (ADMIN 제외)
        total_users = User.objects.exclude(user_type=UserTypeChoices.ADMIN).count()

        # 페이지네이션 적용
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = AdminUserListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)

            # 전체 유저 수 추가
            response_data = paginated_response.data
            response_data['total_users'] = total_users

            return APIResponse.success(
                data=response_data,
                message="유저 목록을 성공적으로 조회했습니다."
            )

        # 페이지네이션이 적용되지 않은 경우
        serializer = AdminUserListSerializer(queryset, many=True)
        return APIResponse.success(
            data={
                'results': serializer.data,
                'total_users': total_users,
                'count': queryset.count()
            },
            message="유저 목록을 성공적으로 조회했습니다."
        )
