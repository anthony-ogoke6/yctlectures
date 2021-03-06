# Generated by Django 2.1 on 2020-08-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0014_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='amountInDols',
            field=models.PositiveIntegerField(default='1'),
        ),
        migrations.AddField(
            model_name='article',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='amountInDols',
            field=models.PositiveIntegerField(default='1'),
        ),
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
