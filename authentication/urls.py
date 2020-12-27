from django.urls import path
from django.conf.urls import url
from authentication.views import RegisterView, VerifyEmail, LoginAPIView, ResetPassword, NewPassword
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view() , name='register'),
    path('login/',LoginAPIView.as_view() , name='login'),
    path('verify-email/',VerifyEmail.as_view() , name='verify-email'),
    path('reset-password/',ResetPassword.as_view() , name='reset-password'),
    path('new-pass/', NewPassword.as_view(), name='new-pass'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
