from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin )
# Create your models here.
# class Registration(models.Model):
    # user_name = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    # date = models.DateTimeField(auto_now_add=True,db_index=True)

 
class UserManager(BaseUserManager):
 
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User should have a username')
        
        if email is None:
            raise TypeError('User should have a Email')
        user = self.model(username=username, email=self.normalize_email)
        user.set_password(password)
        user.save()
        
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password can not be none')

       user = self.create_user(username, email, password)
       user.is_superuser=True
       user.is_staff = True
       user.save()
       return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True,  db_index=True)
    email = models.EmailField(max_length=255, unique=True,  db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    
    def __str__(self):
        return self.email

    def tokens(self):
        return ''
        
