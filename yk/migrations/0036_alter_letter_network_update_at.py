# Generated by Django 3.2.7 on 2021-09-13 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yk', '0035_alter_letter_network_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter_network',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 14, 2, 18, 22, 119354)),
        ),
    ]
