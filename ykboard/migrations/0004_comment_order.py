# Generated by Django 3.2.7 on 2021-09-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ykboard', '0003_auto_20210914_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='order',
            field=models.TextField(default=None, null=True),
        ),
    ]
