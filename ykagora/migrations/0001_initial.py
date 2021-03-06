# Generated by Django 3.2.5 on 2021-07-27 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yk', '0003_auto_20210721_0140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agoraroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agorarooms1', to='yk.profile')),
                ('profile2', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agorarooms2', to='yk.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Agora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=None)),
                ('agoraroom', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agora', to='ykagora.agoraroom')),
                ('pfrom', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='send_agora', to='yk.profile')),
                ('pto', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='receive_agora', to='yk.profile')),
            ],
        ),
    ]
