from django.db import models
from common.models import BaseModel
from users.models import User
from products.models import Product


class Cart(BaseModel):
    """장바구니"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.IntegerField(default=1, verbose_name='수량')

    class Meta:
        db_table = 'carts'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.quantity}개)"


class Wishlist(BaseModel):
    """찜목록/위시리스트"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')

    class Meta:
        db_table = 'wishlists'
        verbose_name = '찜목록'
        verbose_name_plural = '찜목록'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
