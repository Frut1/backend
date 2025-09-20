from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'common'

router = DefaultRouter(trailing_slash=False)
# router.register('', CommonViewSet)

urlpatterns = [
    # path('health', views.HealthCheckView.as_view(), name='health'),
    # path('config', views.ConfigView.as_view(), name='config'),
] + router.urls