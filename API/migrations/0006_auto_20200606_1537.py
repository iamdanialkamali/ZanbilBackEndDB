# Generated by Django 3.0.6 on 2020-06-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_timetable_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sans',
            name='endTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sans',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]
