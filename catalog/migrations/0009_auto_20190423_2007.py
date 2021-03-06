# Generated by Django 2.1.3 on 2019-04-23 17:07

import catalog.models
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0008_auto_20190423_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='location',
            name='inserter',
            field=models.ForeignKey(default=catalog.models.get_empty_user, on_delete=models.SET(catalog.models.get_sentinel_user), related_name='inserted', related_query_name='insert', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='existence',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='existence',
            name='inserter',
        ),
        migrations.AlterUniqueTogether(
            name='existence',
            unique_together={('symbol', 'book')},
        ),
    ]
