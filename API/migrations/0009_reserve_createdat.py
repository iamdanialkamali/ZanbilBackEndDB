
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_auto_20200606_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 15, 17, 30, 50, 856896)),
        ),
    ]
