from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    profile,
    register,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]
