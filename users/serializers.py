from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """회원가입용 시리얼라이저"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    marketing_agreed = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'password', 'password_confirm',
            'marketing_agreed'
        ]

    def validate_username(self, value):
        """아이디 중복 검사"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    def validate_email(self, value):
        """이메일 중복 검사"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def validate_password(self, value):
        """비밀번호 유효성 검사"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


    def validate(self, attrs):
        """비밀번호 확인 검사"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': '비밀번호가 일치하지 않습니다.'
            })
        return attrs

    def create(self, validated_data):
        """사용자 생성"""
        # 불필요한 필드 제거
        validated_data.pop('password_confirm')
        marketing_agreed = validated_data.pop('marketing_agreed', False)

        # 사용자 생성
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            is_marketing_consented=marketing_agreed
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """로그인용 시리얼라이저"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")

            if not user.is_active:
                raise serializers.ValidationError("비활성화된 계정입니다.")

            attrs['user'] = user
            return attrs

        raise serializers.ValidationError("아이디와 비밀번호를 모두 입력해주세요.")


class UserSerializer(serializers.ModelSerializer):
    """사용자 정보용 시리얼라이저"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'email', 'phone', 'profile_image',
            'user_type', 'point_balance', 'is_marketing_consented',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'user_type', 'point_balance', 'date_joined', 'last_login']


class LogoutSerializer(serializers.Serializer):
    """로그아웃용 시리얼라이저"""
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")