
from django.contrib import admin
from django.urls import path
from keep_notes_app import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/',views.registration, name='registration'),
    path('login/',views.loginPage, name='login_url'),
    path('profile/', views.profile, name='profile'),
    path('logout/',views.logoutUser, name='logout'),
]
