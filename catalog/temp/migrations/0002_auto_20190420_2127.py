# Generated by Django 2.1.3 on 2019-04-20 18:27

import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='book_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/vladislav/projects/WebSite/WebSite/catalog/temp/books/'), upload_to='', validators=[django.core.validators.FileExtensionValidator(['txt'])]),
        ),
    ]
