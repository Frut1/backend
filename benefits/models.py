from django.db import models
from common.models import BaseModel
from users.models import User
from orders.models import OrderMain


class CouponTypeChoices(models.TextChoices):
    PERCENTAGE = 'PERCENTAGE', '퍼센트 할인'
    FIXED_AMOUNT = 'FIXED_AMOUNT', '정액 할인'


class PointTypeChoices(models.TextChoices):
    EARN = 'EARN', '적립'
    USE = 'USE', '사용'
    EXPIRE = 'EXPIRE', '만료'


class Coupon(BaseModel):
    """쿠폰 마스터 데이터"""
    
    coupon_name = models.CharField(max_length=100, verbose_name='쿠폰명')
    coupon_code = models.CharField(max_length=50, unique=True, verbose_name='쿠폰 코드')
    coupon_type = models.CharField(
        max_length=15,
        choices=CouponTypeChoices.choices,
        verbose_name='쿠폰 타입'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='할인값')
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='최소 주문 금액')
    usage_limit = models.IntegerField(null=True, blank=True, verbose_name='사용 제한 횟수')
    used_count = models.IntegerField(default=0, verbose_name='사용된 횟수')
    start_date = models.DateTimeField(verbose_name='사용 시작일시')
    end_date = models.DateTimeField(verbose_name='사용 종료일시')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'coupons'
        verbose_name = '쿠폰'
        verbose_name_plural = '쿠폰'

    def __str__(self):
        return self.coupon_name


class UserCoupon(BaseModel):
    """사용자별 쿠폰 보유 현황"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name='쿠폰')
    is_used = models.BooleanField(default=False, verbose_name='사용 여부')
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='사용일시')
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='발급일시')

    class Meta:
        db_table = 'user_coupons'
        verbose_name = '사용자 쿠폰'
        verbose_name_plural = '사용자 쿠폰'

    def __str__(self):
        return f"{self.user.username} - {self.coupon.coupon_name}"


class PointHistory(BaseModel):
    """포인트 적립/사용 이력"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    point_type = models.CharField(
        max_length=10,
        choices=PointTypeChoices.choices,
        verbose_name='포인트 유형'
    )
    point_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='포인트 금액')
    reason = models.CharField(max_length=200, null=True, blank=True, verbose_name='적립/사용 사유')
    order = models.ForeignKey(
        OrderMain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='관련 주문'
    )
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='만료일시')

    class Meta:
        db_table = 'point_histories'
        verbose_name = '포인트 이력'
        verbose_name_plural = '포인트 이력'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.point_type} {self.point_amount}점"
