from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'sellers'

router = DefaultRouter(trailing_slash=False)
# router.register('', SellerViewSet)

urlpatterns = [
    # 농장 관련 API
    path('farms', views.FarmListView.as_view(), name='farm-list'),
    path('farms/<int:farm_id>/follow', views.FarmFollowView.as_view(), name='farm-follow'),
] + router.urls