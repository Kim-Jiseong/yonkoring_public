# Generated by Django 3.2.7 on 2021-09-14 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ykboard', '0002_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('create_at', 'post', 'author')},
        ),
        migrations.RenameField(
            model_name='like',
            old_name='author',
            new_name='user',
        ),
    ]
