from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'operations'

router = DefaultRouter(trailing_slash=False)
# router.register('', OperationViewSet)

urlpatterns = [
    # path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    # path('reports', views.ReportView.as_view(), name='reports'),
] + router.urls