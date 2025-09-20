from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'benefits'

router = DefaultRouter(trailing_slash=False)
# router.register('', BenefitViewSet)

urlpatterns = [
    # path('user', views.UserBenefitListView.as_view(), name='user-benefits'),
    # path('points', views.PointHistoryView.as_view(), name='point-history'),
] + router.urls