# Generated by Django 3.0.6 on 2020-07-06 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_auto_20200705_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='reviewCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 6, 12, 11, 3, 113740)),
        ),
    ]
