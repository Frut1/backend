from django.db import models
from common.models import BaseModel
from users.models import User


class SettlementStatusChoices(models.TextChoices):
    PENDING = 'PENDING', '정산대기'
    COMPLETED = 'COMPLETED', '정산완료'


class Settlement(BaseModel):
    """판매자 매출 정산 관리"""
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='판매자')
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='총 매출액')
    cancelled_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='취소 금액')
    carried_over_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='이월 금액')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='수수료율 (%)')
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='수수료 금액')
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='부가세')
    settlement_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='실제 정산 금액')
    settlement_start_date = models.DateField(verbose_name='정산 시작일')
    settlement_end_date = models.DateField(verbose_name='정산 종료일')
    status = models.CharField(
        max_length=10,
        choices=SettlementStatusChoices.choices,
        default=SettlementStatusChoices.PENDING,
        verbose_name='정산 상태'
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='정산 완료일시')

    class Meta:
        db_table = 'settlements'
        verbose_name = '정산'
        verbose_name_plural = '정산'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.seller.username} - {self.settlement_start_date}~{self.settlement_end_date}"
