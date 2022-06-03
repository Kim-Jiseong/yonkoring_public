# Generated by Django 3.2.5 on 2021-07-27 08:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0004_letter_letter_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter_network',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='Letter_network', to=settings.AUTH_USER_MODEL),
        ),
    ]