
from django.urls import path
from keep_notes_app import views
from django.conf.urls import url
from .views import RegisterView,VerifyEmail



urlpatterns = [
    path('register/',RegisterView.as_view() , name='register'),
    path('verify-email/',VerifyEmail.as_view() , name='email-verify'),
]
