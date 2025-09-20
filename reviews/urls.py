from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'reviews'

router = DefaultRouter(trailing_slash=False)
# router.register('', ReviewViewSet)

urlpatterns = [
    # path('product/<int:product_id>', views.ProductReviewListView.as_view(), name='product-reviews'),
    # path('seller/<int:seller_id>', views.SellerReviewListView.as_view(), name='seller-reviews'),
] + router.urls