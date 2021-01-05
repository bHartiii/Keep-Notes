from django.db import models
from authentication.models import User

# Create your models here.
class Labels(models.Model):
    name = models.TextField(db_index=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def get_name(self):
        return self.name

class Notes(models.Model):
    title=models.TextField()
    content=models.TextField(db_index=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    label = models.ManyToManyField(to=Labels)
    isArchive = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def get_content(self):
        return self.content