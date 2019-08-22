from django.db import models

# Create your models here.

class adm(models.Model):
    pwd = models.CharField(max_length=128)
    fail_count = models.IntegerField()
    is_locked = models.BooleanField()
    lock_datetime = models.DateTimeField(null=True)