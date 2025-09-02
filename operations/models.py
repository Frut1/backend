from django.db import models
from common.models import BaseModel
from users.models import User


class AdTypeChoices(models.TextChoices):
    MAIN = 'MAIN', '메인광고'
    MIDDLE = 'MIDDLE', '중간광고'
    MYPAGE = 'MYPAGE', '마이페이지광고'


class AdStatusChoices(models.TextChoices):
    REVIEW = 'REVIEW', '검토'
    PENDING = 'PENDING', '대기'
    IN_PROGRESS = 'IN_PROGRESS', '진행중'
    COMPLETED = 'COMPLETED', '완료'
    CANCELED = 'CANCELED', '취소'


class BannerAd(BaseModel):
    """메인 배너 광고 관리"""
    
    ad_title = models.CharField(max_length=200, verbose_name='광고 제목')
    ad_company = models.CharField(max_length=50, verbose_name='광고 회사')
    ad_type = models.CharField(
        max_length=10,
        choices=AdTypeChoices.choices,
        verbose_name='광고 유형'
    )
    company_call_number = models.CharField(max_length=50, verbose_name='광고 회사 전화번호')
    company_manager_name = models.CharField(max_length=50, verbose_name='광고 담당자')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='광고 예산')
    inquired_at = models.DateTimeField(verbose_name='문의 일시')
    ad_image = models.CharField(max_length=500, verbose_name='광고 이미지 URL')
    ad_url = models.URLField(null=True, blank=True, verbose_name='클릭시 이동 URL')
    display_order = models.IntegerField(default=0, verbose_name='표시 순서')
    start_date = models.DateTimeField(verbose_name='게시 시작일시')
    end_date = models.DateTimeField(verbose_name='게시 종료일시')
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    click_count = models.IntegerField(default=0, verbose_name='클릭수')
    status = models.CharField(
        max_length=15,
        choices=AdStatusChoices.choices,
        default=AdStatusChoices.REVIEW,
        verbose_name='광고 상태'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='검토 일시')

    class Meta:
        db_table = 'banner_ads'
        verbose_name = '배너 광고'
        verbose_name_plural = '배너 광고'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.ad_title} - {self.ad_company}"


class Popup(BaseModel):
    """팝업 공지사항 관리"""
    
    popup_title = models.CharField(max_length=200, verbose_name='팝업 제목')
    popup_content = models.TextField(verbose_name='팝업 내용')
    popup_image = models.CharField(max_length=500, null=True, blank=True, verbose_name='팝업 이미지')
    start_date = models.DateTimeField(verbose_name='팝업 시작일시')
    end_date = models.DateTimeField(verbose_name='팝업 종료일시')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'popups'
        verbose_name = '팝업'
        verbose_name_plural = '팝업'
        ordering = ['-created_at']

    def __str__(self):
        return self.popup_title


class Policy(BaseModel):
    """서비스 정책 및 약관 관리"""
    
    policy_type = models.CharField(max_length=50, verbose_name='정책 타입')
    policy_title = models.CharField(max_length=200, verbose_name='정책 제목')
    policy_content = models.TextField(verbose_name='정책 내용')
    version = models.CharField(max_length=20, verbose_name='정책 버전')
    is_active = models.BooleanField(default=True, verbose_name='현재 유효한 정책 여부')

    class Meta:
        db_table = 'policies'
        verbose_name = '정책'
        verbose_name_plural = '정책'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.policy_type} - {self.policy_title} (v{self.version})"
