#coding=utf-8
from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    user = models.CharField(max_length=18)
    pwd = models.CharField(max_length=32)
    money = models.FloatField()
    final_login = models.DateTimeField(null=True)

class Requests(models.Model):
    request = models.ForeignKey(to='Request', to_field='rid', on_delete=models.CASCADE)

class Request(models.Model):
    rid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='User', to_field='uid', on_delete=models.CASCADE)
    money = models.FloatField()
    request_datetime = models.DateTimeField(auto_now_add=True)
    # 1:借 2:还 3:待定 4:不见
    request_type = models.IntegerField(null=True)
    ps = models.CharField(max_length=64, null=True)

class RegisterCode(models.Model):
    code = models.CharField(max_length=20, db_index=True)