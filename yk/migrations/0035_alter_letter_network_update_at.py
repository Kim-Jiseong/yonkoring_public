# Generated by Django 3.2.7 on 2021-09-13 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yk', '0034_alter_letter_network_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter_network',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 14, 1, 49, 13, 366930)),
        ),
    ]