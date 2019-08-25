from django.db import models

# Create your models here.

class Articles(models.Model):
    aid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, db_index=True)
    content = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    imgs = models.CharField(max_length=1024, null=True)

class Tags(models.Model):
    tid = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=18)

class ArticlesToTags(models.Model):
    article = models.ForeignKey(to='Articles', to_field='aid', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tags', to_field='tid', on_delete=models.CASCADE)