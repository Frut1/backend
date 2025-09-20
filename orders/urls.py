from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'orders'

router = DefaultRouter(trailing_slash=False)
# router.register('', OrderViewSet)

urlpatterns = [
    # path('create', views.CreateOrderView.as_view(), name='create'),
    # path('<int:order_id>/cancel', views.CancelOrderView.as_view(), name='cancel'),
    # path('<int:order_id>/payment', views.PaymentView.as_view(), name='payment'),
] + router.urls