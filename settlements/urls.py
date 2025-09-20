from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'settlements'

router = DefaultRouter(trailing_slash=False)
# router.register('', SettlementViewSet)

urlpatterns = [
    # path('seller/<int:seller_id>', views.SellerSettlementView.as_view(), name='seller-settlement'),
    # path('history', views.SettlementHistoryView.as_view(), name='history'),
] + router.urls