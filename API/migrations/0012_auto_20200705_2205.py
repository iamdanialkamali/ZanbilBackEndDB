# Generated by Django 3.0.6 on 2020-07-05 22:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_auto_20200705_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 5, 22, 5, 28, 289805)),
        ),
    ]
