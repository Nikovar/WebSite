# Generated by Django 2.1.3 on 2019-04-03 20:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_auto_20190403_2309'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Existences',
            new_name='Existence',
        ),
    ]

    atomic = False
