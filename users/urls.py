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
    path('auth/withdraw', views.WithdrawView.as_view(), name='withdraw'),
    path('auth/change-password', views.PasswordChangeView.as_view(), name='change_password'),

    # Admin endpoints
    path('admin/list', views.AdminUserListView.as_view(), name='admin_user_list'),
] + router.urls