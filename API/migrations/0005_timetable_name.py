# Generated by Django 3.0.6 on 2020-06-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20200606_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='name',
            field=models.CharField(default='timeTable', max_length=30),
        ),
    ]
