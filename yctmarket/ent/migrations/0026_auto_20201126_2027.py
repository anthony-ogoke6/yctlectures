# Generated by Django 2.1 on 2020-11-26 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0025_auto_20201125_0350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='post',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]