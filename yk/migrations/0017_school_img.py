# Generated by Django 3.2.6 on 2021-08-04 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0016_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='School_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='school_images/')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_img', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]