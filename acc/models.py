from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=12)
    pwd = models.CharField(max_length=32)
    money = models.FloatField()
    final_login = models.DateTimeField()

class Request(models.Model):
    rid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='User', to_field='uid', on_delete=models.CASCADE)
    money = models.FloatField()
    request_datetime = models.DateTimeField(auto_now_add=True)

class RegisterCode(models.Model):
    code = models.CharField(max_length=20)
    status = models.BooleanField()