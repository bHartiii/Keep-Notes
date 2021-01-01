from django.db import models
from authentication.models import User

# Create your models here.
class Labels(models.Model):
    name = models.TextField(db_index=True, unique=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
class Notes(models.Model):
    title=models.TextField()
    content=models.TextField(db_index=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    label = models.ForeignKey(to=Labels, on_delete=models.CASCADE)
    isArchive = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True, null=False, blank=False)

