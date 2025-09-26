from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserTypeChoices


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


class UserWithdrawalSerializer(serializers.Serializer):
    """회원 탈퇴용 시리얼라이저"""
    password = serializers.CharField(write_only=True)
    withdrawal_reason = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="탈퇴 사유 (선택사항)"
    )
    agree_withdrawal = serializers.BooleanField(
        help_text="탈퇴에 동의합니다"
    )

    def validate_password(self, value):
        """현재 비밀번호 확인"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value

    def validate_agree_withdrawal(self, value):
        """탈퇴 동의 확인"""
        if not value:
            raise serializers.ValidationError("탈퇴에 동의해주세요.")
        return value

    def save(self, **kwargs):
        """사용자 탈퇴 처리"""
        from django.utils import timezone
        from .models import UserStatusChoices

        user = self.context['request'].user

        # 사용자 상태를 탈퇴로 변경
        user.status = UserStatusChoices.WITHDRAWN
        user.withdrawn_at = timezone.now()
        user.is_active = False
        user.save()

        return user


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경용 시리얼라이저"""
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        """현재 비밀번호 확인"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value

    def validate_new_password(self, value):
        """새 비밀번호 유효성 검사"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """비밀번호 확인 및 중복 검사"""
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        # 새 비밀번호 확인 일치 검사
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': '새 비밀번호가 일치하지 않습니다.'
            })

        # 현재 비밀번호와 새 비밀번호 동일성 검사
        if current_password == new_password:
            raise serializers.ValidationError({
                'new_password': '새 비밀번호는 현재 비밀번호와 달라야 합니다.'
            })

        return attrs

    def save(self, **kwargs):
        """비밀번호 변경"""
        user = self.context['request'].user
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return user


class AdminUserListSerializer(serializers.ModelSerializer):
    """관리자 페이지용 유저 목록 시리얼라이저"""
    nickname = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'name', 'nickname', 'username', 'email',
            'user_type', 'is_seller', 'status', 'status_display',
            'date_joined'
        ]

    def get_nickname(self, obj):
        """닉네임 반환 - SELLER인 경우 farm_name, 아닌 경우 '-'"""
        if obj.user_type == UserTypeChoices.SELLER:
            # FarmProfile이 있는지 확인 후 farm_name 반환
            if hasattr(obj, 'farmprofile') and obj.farmprofile.farm_name:
                return obj.farmprofile.farm_name
            return '-'
        return '-'

    def get_is_seller(self, obj):
        """판매자 여부 - 판매자면 O, 아니면 X"""
        return 'O' if obj.user_type == UserTypeChoices.SELLER else 'X'

    def get_date_joined(self, obj):
        """가입일을 25.01.01 형식으로 반환"""
        return obj.date_joined.strftime('%y.%m.%d')