# Generated by Django 2.1 on 2020-06-02 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0006_auto_20200602_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stores',
            old_name='store_name',
            new_name='storename',
        ),
    ]
