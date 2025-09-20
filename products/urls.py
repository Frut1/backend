from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'products'

router = DefaultRouter(trailing_slash=False)
# router.register('', ProductViewSet)

urlpatterns = [
    # path('categories', views.CategoryListView.as_view(), name='category-list'),
    # path('search', views.ProductSearchView.as_view(), name='search'),
] + router.urls