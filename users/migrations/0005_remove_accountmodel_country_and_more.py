# Generated by Django 5.0.6 on 2024-06-15 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_accountmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountmodel',
            name='country',
        ),
        migrations.RemoveField(
            model_name='accountmodel',
            name='postcode',
        ),
        migrations.AlterField(
            model_name='accountmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]