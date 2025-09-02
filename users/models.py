from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel


class UserTypeChoices(models.TextChoices):
    CONSUMER = 'CONSUMER', '소비자'
    SELLER = 'SELLER', '판매자'
    ADMIN = 'ADMIN', '관리자'


class SnsTypeChoices(models.TextChoices):
    NONE = 'NONE', '일반 회원가입'
    NAVER = 'NAVER', '네이버 로그인'
    KAKAO = 'KAKAO', '카카오 로그인'


class UserStatusChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', '활성 상태'
    WITHDRAWN = 'WITHDRAWN', '탈퇴 상태'
    BLOCKED = 'BLOCKED', '차단 상태'


class User(AbstractUser, BaseModel):
    """플랫폼 사용자 (소비자/판매자/관리자) 기본 정보"""
    
    # AbstractUser의 username을 그대로 사용 (ID 역할)
    email = models.EmailField(unique=True, verbose_name='이메일')
    name = models.CharField(max_length=100, verbose_name='실명')
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='전화번호')
    profile_image = models.CharField(max_length=500, null=True, blank=True, verbose_name='프로필 이미지 URL')
    user_note = models.TextField(null=True, blank=True, verbose_name='메모')
    user_type = models.CharField(
        max_length=10,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.CONSUMER,
        verbose_name='사용자 타입'
    )
    sns_type = models.CharField(
        max_length=10,
        choices=SnsTypeChoices.choices,
        default=SnsTypeChoices.NONE,
        verbose_name='SNS 연동 타입'
    )
    sns_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='SNS 고유 ID')
    point_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='포인트 잔액')
    status = models.CharField(
        max_length=10,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.ACTIVE,
        verbose_name='계정 상태'
    )
    is_marketing_consented = models.BooleanField(default=False, verbose_name='마케팅 수신 동의')
    withdrawn_at = models.DateTimeField(null=True, blank=True, verbose_name='비활성화 일시')
    blocked_at = models.DateTimeField(null=True, blank=True, verbose_name='차단 일시')

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return f"{self.username} ({self.name})"


class UserAddress(BaseModel):
    """사용자 배송지 관리"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    address_name = models.CharField(max_length=50, verbose_name='주소별명')
    recipient_name = models.CharField(max_length=100, verbose_name='수령인 이름')
    recipient_phone = models.CharField(max_length=20, verbose_name='수령인 전화번호')
    zipcode = models.CharField(max_length=10, verbose_name='우편번호')
    address = models.CharField(max_length=200, verbose_name='기본 주소')
    detail_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='상세 주소')
    is_default = models.BooleanField(default=False, verbose_name='기본 배송지 여부')

    class Meta:
        db_table = 'user_addresses'
        verbose_name = '사용자 주소'
        verbose_name_plural = '사용자 주소'

    def __str__(self):
        return f"{self.user.username} - {self.address_name}"
