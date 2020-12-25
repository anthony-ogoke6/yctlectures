# Generated by Django 2.1 on 2020-12-08 12:36

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0026_auto_20201126_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertimages',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='advertimages',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, default='2020-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
