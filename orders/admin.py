from django.contrib import admin
from .models import OrderMain, OrderItem, Delivery


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(OrderMain)
class OrderMainAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'final_amount', 'order_status', 'ordered_at')
    list_filter = ('order_status', 'ordered_at')
    search_fields = ('order_number', 'user__username', 'recipient_name')
    readonly_fields = ('ordered_at', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('주문 정보', {
            'fields': ('order_number', 'user', 'order_status', 'ordered_at')
        }),
        ('금액 정보', {
            'fields': ('total_amount', 'discount_amount', 'point_used', 'final_amount')
        }),
        ('배송 정보', {
            'fields': ('recipient_name', 'recipient_phone', 'delivery_address')
        }),
        ('기타', {
            'fields': ('order_memo', 'confirmed_at', 'shipped_at', 'delivered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'seller', 'quantity', 'total_price', 'item_status')
    list_filter = ('item_status',)
    search_fields = ('order__order_number', 'product_name', 'seller__username')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_company', 'tracking_number', 'delivery_status', 'shipped_at')
    list_filter = ('delivery_status', 'delivery_company')
    search_fields = ('order__order_number', 'tracking_number')
