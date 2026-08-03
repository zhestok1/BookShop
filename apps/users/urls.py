from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from apps.users.views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    VerifyEmailView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='register'),
    path('verification/', VerifyEmailView.as_view(), name='verification'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


