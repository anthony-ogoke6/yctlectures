# Generated by Django 2.1 on 2020-11-25 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0024_phonenumber_matric_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stores',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Stores',
        ),
    ]
