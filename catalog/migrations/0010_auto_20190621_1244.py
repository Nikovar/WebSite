# Generated by Django 2.1.3 on 2019-06-21 09:44

import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20190423_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='book',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='language',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='location',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='symbol',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='symboldescription',
            name='checked',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(help_text='Upload your text of book in one single file here', storage=django.core.files.storage.FileSystemStorage(location='/home/gronix/code/git/study/WebSite/catalog/books/'), upload_to='', validators=[django.core.validators.FileExtensionValidator(['txt'])]),
        ),
    ]
