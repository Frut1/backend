from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

router = DefaultRouter(trailing_slash=False)
# router.register('', UserViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('auth/refresh', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
] + router.urls