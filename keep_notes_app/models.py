from django.db import models

# Create your models here.
class Registration(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True,db_index=True)