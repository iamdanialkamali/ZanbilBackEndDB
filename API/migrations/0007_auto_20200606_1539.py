# Generated by Django 3.0.6 on 2020-06-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_auto_20200606_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sans',
            name='endTime',
            field=models.CharField(default='00:00', max_length=5),
        ),
        migrations.AlterField(
            model_name='sans',
            name='startTime',
            field=models.CharField(default='00:00', max_length=5),
        ),
    ]
