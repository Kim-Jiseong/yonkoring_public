# Generated by Django 3.2.6 on 2021-08-07 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0017_school_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Want_gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=20, null=True, verbose_name='성별')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='want_gender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
