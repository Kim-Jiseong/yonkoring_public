# Generated by Django 3.2.7 on 2021-09-14 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ykboard', '0004_comment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
