# Generated by Django 2.1 on 2020-08-26 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0016_auto_20200820_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertimages',
            name='pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
