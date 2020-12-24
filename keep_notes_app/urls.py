
from django.urls import path
from keep_notes_app import views
from django.conf.urls import url
from .views import RegisterView, VerifyEmail, LoginView



urlpatterns = [
    path('register/',RegisterView.as_view() , name='register'),
    path('login/',LoginView.as_view() , name='login'),
    path('verify-email/',VerifyEmail.as_view() , name='verify-email'),
]
