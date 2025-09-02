from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'name', 'user_type', 'status', 'date_joined')
    list_filter = ('user_type', 'status', 'sns_type', 'is_marketing_consented')
    search_fields = ('username', 'email', 'name', 'phone')
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('name', 'phone', 'profile_image', 'user_note', 'user_type')
        }),
        ('SNS 정보', {
            'fields': ('sns_type', 'sns_id')
        }),
        ('포인트 & 상태', {
            'fields': ('point_balance', 'status', 'is_marketing_consented')
        }),
        ('중요 날짜', {
            'fields': ('withdrawn_at', 'blocked_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_name', 'recipient_name', 'is_default', 'created_at')
    list_filter = ('is_default',)
    search_fields = ('user__username', 'recipient_name', 'address')
    readonly_fields = ('created_at', 'updated_at')
