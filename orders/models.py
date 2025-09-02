from django.db import models
from common.models import BaseModel
from users.models import User
from products.models import Product


class OrderStatusChoices(models.TextChoices):
    PENDING = 'PENDING', '주문접수'
    CONFIRMED = 'CONFIRMED', '주문확인'
    SHIPPED = 'SHIPPED', '배송중'
    DELIVERED = 'DELIVERED', '배송완료'
    CANCELLED = 'CANCELLED', '주문취소'
    REFUNDED = 'REFUNDED', '환불완료'


class DeliveryStatusChoices(models.TextChoices):
    PREPARING = 'PREPARING', '배송준비중'
    SHIPPED = 'SHIPPED', '배송중'
    IN_TRANSIT = 'IN_TRANSIT', '배송중'
    DELIVERED = 'DELIVERED', '배송완료'


class OrderMain(BaseModel):
    """주문 메인 정보"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='주문자')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='주문번호')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='주문 총액')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='할인 금액')
    point_used = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='사용 포인트')
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='최종 결제 금액')
    order_status = models.CharField(
        max_length=10,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
        verbose_name='주문 상태'
    )
    recipient_name = models.CharField(max_length=100, verbose_name='수령인 이름')
    recipient_phone = models.CharField(max_length=20, verbose_name='수령인 전화번호')
    delivery_address = models.CharField(max_length=500, verbose_name='배송 주소')
    order_memo = models.TextField(null=True, blank=True, verbose_name='주문 메모')
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name='주문일시')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='주문확인일시')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='출고일시')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='배송완료일시')

    class Meta:
        db_table = 'order_mains'
        verbose_name = '주문'
        verbose_name_plural = '주문'
        ordering = ['-ordered_at']

    def __str__(self):
        return f"{self.order_number} - {self.user.username}"


class OrderItem(BaseModel):
    """주문 상품 상세 정보"""
    
    order = models.ForeignKey(OrderMain, on_delete=models.CASCADE, verbose_name='주문')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='판매자')
    product_name = models.CharField(max_length=200, verbose_name='주문 당시 상품명')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='단가')
    quantity = models.IntegerField(verbose_name='주문 수량')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='소계')
    item_status = models.CharField(
        max_length=10,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
        verbose_name='상품별 주문 상태'
    )

    class Meta:
        db_table = 'order_items'
        verbose_name = '주문 상품'
        verbose_name_plural = '주문 상품'

    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"


class Delivery(BaseModel):
    """배송 정보"""
    
    order = models.OneToOneField(OrderMain, on_delete=models.CASCADE, verbose_name='주문')
    delivery_company = models.CharField(max_length=50, null=True, blank=True, verbose_name='택배회사명')
    tracking_number = models.CharField(max_length=100, null=True, blank=True, verbose_name='송장번호')
    delivery_status = models.CharField(
        max_length=15,
        choices=DeliveryStatusChoices.choices,
        default=DeliveryStatusChoices.PREPARING,
        verbose_name='배송 상태'
    )
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='출고일시')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='배송완료일시')

    class Meta:
        db_table = 'deliveries'
        verbose_name = '배송'
        verbose_name_plural = '배송'

    def __str__(self):
        return f"{self.order.order_number} - {self.delivery_status}"
