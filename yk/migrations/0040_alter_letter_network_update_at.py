# Generated by Django 3.2.7 on 2021-09-17 04:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yk', '0039_alter_letter_network_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter_network',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 13, 53, 24, 204861)),
        ),
    ]
