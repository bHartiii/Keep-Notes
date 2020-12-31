from django.db import models
from authentication.models import User

# Create your models here.
class Notes(models.Model):
    title=models.TextField()
    content=models.TextField(db_index=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    isArchive = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True, null=False, blank=False)