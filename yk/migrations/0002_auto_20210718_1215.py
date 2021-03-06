# Generated by Django 3.2.5 on 2021-07-18 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='위도'),
        ),
        migrations.AddField(
            model_name='profile',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='경도'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=150, null=True, verbose_name='친구 신청 메시지')),
                ('message_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to=settings.AUTH_USER_MODEL)),
                ('message_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_report', to=settings.AUTH_USER_MODEL)),
                ('message_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=100, null=True, verbose_name='question')),
                ('ask_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask_from', to=settings.AUTH_USER_MODEL)),
                ('ask_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ask_report', to=settings.AUTH_USER_MODEL)),
                ('ask_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='answer')),
                ('answered_at', models.DateField(auto_now_add=True, null=True)),
                ('ask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask', to='yk.ask')),
            ],
        ),
    ]
