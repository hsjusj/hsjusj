# Generated by Django 2.2.2 on 2019-08-24 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0002_auto_20190824_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=18),
        ),
    ]
