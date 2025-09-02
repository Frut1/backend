from django.contrib import admin
from .models import (
    SellerApplication, SellerFile, FarmProfile, 
    FarmNews, FarmNewsImage, FarmFollow
)


@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'status', 'applied_at', 'processed_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'business_name', 'business_number')
    readonly_fields = ('applied_at', 'processed_at', 'created_at', 'updated_at')
    
    fieldsets = (
        ('신청자 정보', {
            'fields': ('user', 'status', 'applied_at', 'processed_at', 'processed_by')
        }),
        ('사업체 정보', {
            'fields': ('business_name', 'business_number', 'representative_name')
        }),
        ('연락처 정보', {
            'fields': ('business_address', 'business_phone')
        }),
        ('기타', {
            'fields': ('application_reason',)
        }),
    )


@admin.register(FarmProfile)
class FarmProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_name', 'location', 'follower_count', 'created_at')
    search_fields = ('user__username', 'farm_name', 'location')
    readonly_fields = ('follower_count', 'created_at', 'updated_at')


class FarmNewsImageInline(admin.TabularInline):
    model = FarmNewsImage
    extra = 1


@admin.register(FarmNews)
class FarmNewsAdmin(admin.ModelAdmin):
    list_display = ('farm', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('farm__farm_name', 'title')
    inlines = [FarmNewsImageInline]


@admin.register(FarmFollow)
class FarmFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm', 'followed_at')
    list_filter = ('followed_at',)
    search_fields = ('user__username', 'farm__farm_name')
