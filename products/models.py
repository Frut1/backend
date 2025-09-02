from django.db import models
from common.models import BaseModel
from sellers.models import FarmProfile


class ProductStatusChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', '판매중'
    INACTIVE = 'INACTIVE', '판매중단'
    OUT_OF_STOCK = 'OUT_OF_STOCK', '품절'


class SpecialStatusChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', '특가진행중'
    INACTIVE = 'INACTIVE', '특가중단'
    EXPIRED = 'EXPIRED', '특가종료'


class Category(BaseModel):
    """상품 카테고리 (계층구조)"""
    
    category_name = models.CharField(max_length=100, verbose_name='카테고리명')
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='부모 카테고리'
    )
    sort_order = models.IntegerField(default=0, verbose_name='정렬 순서')
    is_active = models.BooleanField(default=True, verbose_name='사용 여부')

    class Meta:
        db_table = 'categories'
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
        ordering = ['sort_order', 'category_name']

    def __str__(self):
        return self.category_name


class Product(BaseModel):
    """농산물 상품 정보"""
    
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, verbose_name='판매자 농장')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='카테고리')
    product_name = models.CharField(max_length=200, verbose_name='상품명')
    product_description = models.TextField(null=True, blank=True, verbose_name='상품 설명')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='기본가격')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='할인율 (%)')
    stock_quantity = models.IntegerField(default=0, verbose_name='재고 수량')
    producer_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='생산자명')
    producer_location = models.CharField(max_length=200, null=True, blank=True, verbose_name='생산지/소재지')
    production_date = models.DateField(null=True, blank=True, verbose_name='제조연월일/포장일')
    production_year = models.IntegerField(null=True, blank=True, verbose_name='생산연도')
    expiry_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='유통기한 유형')
    legal_notice = models.TextField(null=True, blank=True, verbose_name='관련법상 표시사항')
    product_composition = models.TextField(null=True, blank=True, verbose_name='상품구성 정보')
    handling_method = models.TextField(null=True, blank=True, verbose_name='취급방법')
    customer_service_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='소비자상담 전화번호')
    status = models.CharField(
        max_length=15,
        choices=ProductStatusChoices.choices,
        default=ProductStatusChoices.ACTIVE,
        verbose_name='상품 상태'
    )
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='평균 평점')
    review_count = models.IntegerField(default=0, verbose_name='리뷰 개수')

    class Meta:
        db_table = 'products'
        verbose_name = '상품'
        verbose_name_plural = '상품'
        ordering = ['-created_at']

    def __str__(self):
        return self.product_name


class ProductOption(models.Model):
    """상품 옵션"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    name = models.CharField(max_length=50, verbose_name='옵션명')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='옵션가격')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='할인율 (%)')

    class Meta:
        db_table = 'product_options'
        verbose_name = '상품 옵션'
        verbose_name_plural = '상품 옵션'

    def __str__(self):
        return f"{self.product.product_name} - {self.name}"


class ProductImage(BaseModel):
    """상품 이미지 관리"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    image_url = models.CharField(max_length=500, verbose_name='이미지 URL')
    sort_order = models.IntegerField(default=0, verbose_name='표시 순서')
    is_main = models.BooleanField(default=False, verbose_name='대표 이미지 여부')

    class Meta:
        db_table = 'product_images'
        verbose_name = '상품 이미지'
        verbose_name_plural = '상품 이미지'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.product_name} - 이미지 {self.sort_order}"


class ProductBadge(models.Model):
    """상품 배지 마스터 데이터"""
    
    badge_name = models.CharField(max_length=50, verbose_name='배지명')
    image_url = models.CharField(max_length=100, verbose_name='배지 이미지 URL')
    is_active = models.BooleanField(default=True, verbose_name='사용 여부')

    class Meta:
        db_table = 'product_badges'
        verbose_name = '상품 배지'
        verbose_name_plural = '상품 배지'

    def __str__(self):
        return self.badge_name


class ProductBadgeMapping(BaseModel):
    """상품-배지 매핑 테이블"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    badge = models.ForeignKey(ProductBadge, on_delete=models.CASCADE, verbose_name='배지')

    class Meta:
        db_table = 'product_badge_mappings'
        verbose_name = '상품 배지 매핑'
        verbose_name_plural = '상품 배지 매핑'
        unique_together = ['product', 'badge']

    def __str__(self):
        return f"{self.product.product_name} - {self.badge.badge_name}"


class SpecialProduct(BaseModel):
    """한정 특가 상품 관리"""
    
    product_name = models.CharField(max_length=200, verbose_name='특가상품명')
    product_description = models.TextField(null=True, blank=True, verbose_name='상품 설명')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='원래 가격')
    special_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='특가 가격')
    stock_quantity = models.IntegerField(default=0, verbose_name='재고 수량')
    start_date = models.DateTimeField(verbose_name='특가 시작일시')
    end_date = models.DateTimeField(verbose_name='특가 종료일시')
    status = models.CharField(
        max_length=10,
        choices=SpecialStatusChoices.choices,
        default=SpecialStatusChoices.ACTIVE,
        verbose_name='특가 상태'
    )
    product_image = models.CharField(max_length=500, null=True, blank=True, verbose_name='상품 이미지')

    class Meta:
        db_table = 'special_products'
        verbose_name = '특가 상품'
        verbose_name_plural = '특가 상품'
        ordering = ['-created_at']

    def __str__(self):
        return self.product_name
