from django.urls import path


from authentication.views import RegisterView, VerifyEmail, LoginAPIView, ResetPassword, NewPassword, LogoutView, UserProfileView

urlpatterns = [
    path('register/',RegisterView.as_view() , name='register'),
    path('user-profile/', UserProfileView.as_view(), name= 'user-profile'),
    path('login/',LoginAPIView.as_view() , name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/',VerifyEmail.as_view() , name='verify-email'),
    path('reset-password/',ResetPassword.as_view() , name='reset-password'),
    path('new-pass/', NewPassword.as_view(), name='new-pass'),
    
]