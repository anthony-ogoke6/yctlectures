# Generated by Django 2.1 on 2021-08-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0049_donationreference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donationreference',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='donationreference',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]