# Generated by Django 2.1 on 2021-08-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0047_auto_20210812_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='images/default1.jpng', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image2',
            field=models.ImageField(blank=True, default='images/default1.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image3',
            field=models.ImageField(blank=True, default='images/default1.png', null=True, upload_to='images/'),
        ),
    ]
