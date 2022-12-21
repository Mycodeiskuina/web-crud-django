from django.db import models

from django.conf import settings

# Create your models here.

class Task(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    course = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    done = models.BooleanField(default=False)
    class Meta:
        db_table = 'Tasks'
