from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.response import APIResponse
from common.mixins import StandardAPIViewMixin
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    LogoutSerializer
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
