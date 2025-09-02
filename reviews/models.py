from django.db import models
from common.models import BaseModel
from users.models import User
from products.models import Product
from orders.models import OrderItem


class Review(BaseModel):
    """상품 리뷰"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='리뷰어')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, verbose_name='주문상품')
    rating = models.IntegerField(verbose_name='평점 (1-5)')
    review_content = models.TextField(null=True, blank=True, verbose_name='리뷰 내용')
    review_image = models.CharField(max_length=500, null=True, blank=True, verbose_name='리뷰 이미지')

    class Meta:
        db_table = 'reviews'
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.rating}점)"
