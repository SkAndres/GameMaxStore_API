# Generated by Django 4.0.6 on 2022-08-01 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_auth_provider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auth_provider',
        ),
    ]
