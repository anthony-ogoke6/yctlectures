# Generated by Django 2.1 on 2020-12-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0027_auto_20201208_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
