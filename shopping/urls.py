from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'shopping'

router = DefaultRouter(trailing_slash=False)
# router.register('cart', CartViewSet)
# router.register('wishlist', WishlistViewSet)

urlpatterns = [
    # path('cart/add', views.AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/remove', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
] + router.urls