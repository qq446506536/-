# Generated by Django 2.0.6 on 2018-07-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20180712_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='img',
            field=models.CharField(default='/static/default.jpg', max_length=128),
        ),
    ]