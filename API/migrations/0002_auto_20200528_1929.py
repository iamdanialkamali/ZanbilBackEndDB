# Generated by Django 3.0.6 on 2020-05-28 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='date',
            field=models.DateTimeField(max_length=150),
        ),
    ]
