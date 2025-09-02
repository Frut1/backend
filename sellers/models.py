from django.db import models
from common.models import BaseModel
from users.models import User


class ApplicationStatusChoices(models.TextChoices):
    PENDING = 'PENDING', '검토 중'
    APPROVED = 'APPROVED', '승인'
    REJECTED = 'REJECTED', '거부'


class FileKindsChoices(models.TextChoices):
    사업자등록증 = '사업자등록증', '사업자등록증'
    통신판매업신고증 = '통신판매업신고증', '통신판매업신고증'
    대표자신분증사본 = '대표자신분증사본', '대표자신분증사본'
    통장사본 = '통장사본', '통장사본'
    농장프로필사진 = '농장프로필사진', '농장프로필사진'
    GAP인증서 = 'GAP인증서', 'GAP인증서'
    유기농인증서 = '유기농인증서', '유기농인증서'
    HACCP인증서 = 'HACCP인증서', 'HACCP인증서'
    잔류농약검사서 = '잔류농약검사서', '잔류농약검사서'


class FileStatusChoices(models.TextChoices):
    PENDING = 'PENDING', '검토 중'
    APPROVED = 'APPROVED', '승인'
    REJECTED = 'REJECTED', '거부'


class SellerApplication(BaseModel):
    """판매자 등록 신청 관리"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='신청자')
    business_name = models.CharField(max_length=100, verbose_name='사업체명/농장명')
    business_number = models.CharField(max_length=20, verbose_name='사업자등록번호')
    representative_name = models.CharField(max_length=100, verbose_name='대표자명')
    business_address = models.CharField(max_length=300, verbose_name='사업장 주소')
    business_phone = models.CharField(max_length=20, verbose_name='사업장 전화번호')
    application_reason = models.TextField(null=True, blank=True, verbose_name='판매자 신청 사유')
    status = models.CharField(
        max_length=10,
        choices=ApplicationStatusChoices.choices,
        default=ApplicationStatusChoices.PENDING,
        verbose_name='승인 상태'
    )
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name='신청일시')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='처리일시')
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_applications',
        verbose_name='처리한 관리자'
    )

    class Meta:
        db_table = 'seller_applications'
        verbose_name = '판매자 신청'
        verbose_name_plural = '판매자 신청'

    def __str__(self):
        return f"{self.user.username} - {self.business_name}"


class SellerFile(BaseModel):
    """판매자 서류"""
    
    application = models.ForeignKey(SellerApplication, on_delete=models.CASCADE, verbose_name='신청서')
    kinds = models.CharField(
        max_length=20,
        choices=FileKindsChoices.choices,
        verbose_name='파일 종류'
    )
    status = models.CharField(
        max_length=10,
        choices=FileStatusChoices.choices,
        default=FileStatusChoices.PENDING,
        verbose_name='승인 상태'
    )
    rejected_reason = models.TextField(null=True, blank=True, verbose_name='반려 사유')

    class Meta:
        db_table = 'seller_files'
        verbose_name = '판매자 서류'
        verbose_name_plural = '판매자 서류'

    def __str__(self):
        return f"{self.application.business_name} - {self.kinds}"


class FarmProfile(BaseModel):
    """판매자 농장 프로필 정보"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='판매자')
    farm_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='농장 상호명')
    farm_description = models.TextField(null=True, blank=True, verbose_name='농장 소개')
    farm_image = models.CharField(max_length=500, null=True, blank=True, verbose_name='농장 대표 이미지')
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name='농장 위치')
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='농장 연락처')
    contact_email = models.EmailField(null=True, blank=True, verbose_name='농장 이메일')
    follower_count = models.IntegerField(default=0, verbose_name='팔로워 수')

    class Meta:
        db_table = 'farm_profiles'
        verbose_name = '농장 프로필'
        verbose_name_plural = '농장 프로필'

    def __str__(self):
        return f"{self.user.username} - {self.farm_name or '농장명 없음'}"


class FarmNews(BaseModel):
    """농장 소식/뉴스 관리"""
    
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, verbose_name='농장')
    title = models.CharField(max_length=200, verbose_name='농장소식 제목')
    content = models.TextField(verbose_name='농장소식 내용')
    url = models.URLField(null=True, blank=True, verbose_name='URL')

    class Meta:
        db_table = 'farm_news'
        verbose_name = '농장 소식'
        verbose_name_plural = '농장 소식'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farm.farm_name} - {self.title}"


class FarmNewsImage(models.Model):
    """농장 소식 첨부 이미지"""
    
    news = models.ForeignKey(FarmNews, on_delete=models.CASCADE, verbose_name='농장 소식')
    image_url = models.CharField(max_length=500, verbose_name='첨부 이미지 URL')

    class Meta:
        db_table = 'farm_news_images'
        verbose_name = '농장소식 이미지'
        verbose_name_plural = '농장소식 이미지'

    def __str__(self):
        return f"{self.news.title} - 이미지"


class FarmFollow(BaseModel):
    """농장 팔로우 관계"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='팔로워')
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, verbose_name='농장')
    followed_at = models.DateTimeField(auto_now_add=True, verbose_name='팔로우 일시')

    class Meta:
        db_table = 'farm_follows'
        verbose_name = '농장 팔로우'
        verbose_name_plural = '농장 팔로우'
        unique_together = ['user', 'farm']

    def __str__(self):
        return f"{self.user.username} → {self.farm.farm_name}"
