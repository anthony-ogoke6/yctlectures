# Generated by Django 2.1 on 2020-06-02 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0008_auto_20200602_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='stores',
            name='description',
            field=models.TextField(default=''),
        ),
    ]