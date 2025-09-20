from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'sellers'

router = DefaultRouter(trailing_slash=False)
# router.register('', SellerViewSet)

urlpatterns = [
    # path('profile', views.SellerProfileView.as_view(), name='profile'),
    # path('farms', views.FarmListView.as_view(), name='farm-list'),
] + router.urls