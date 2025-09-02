from django.contrib import admin
from .models import (
    Category, Product, ProductOption, ProductImage, 
    ProductBadge, ProductBadgeMapping, SpecialProduct
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent_category', 'sort_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent_category')
    search_fields = ('category_name',)
    ordering = ['sort_order', 'category_name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('created_at',)


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'farm', 'category', 'price', 'stock_quantity', 'status', 'created_at')
    list_filter = ('status', 'category', 'farm')
    search_fields = ('product_name', 'farm__farm_name', 'producer_name')
    readonly_fields = ('view_count', 'rating_avg', 'review_count', 'created_at', 'updated_at')
    inlines = [ProductImageInline, ProductOptionInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('product_name', 'farm', 'category', 'product_description', 'status')
        }),
        ('가격 및 재고', {
            'fields': ('price', 'discount_rate', 'stock_quantity')
        }),
        ('생산 정보', {
            'fields': ('producer_name', 'producer_location', 'production_date', 'production_year')
        }),
        ('상품 상세', {
            'fields': ('expiry_type', 'legal_notice', 'product_composition', 'handling_method', 'customer_service_phone')
        }),
        ('통계', {
            'fields': ('view_count', 'rating_avg', 'review_count')
        }),
    )


@admin.register(ProductBadge)
class ProductBadgeAdmin(admin.ModelAdmin):
    list_display = ('badge_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('badge_name',)


@admin.register(SpecialProduct)
class SpecialProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'original_price', 'special_price', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('product_name',)
    readonly_fields = ('created_at', 'updated_at')
