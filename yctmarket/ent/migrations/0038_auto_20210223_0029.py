# Generated by Django 2.1 on 2021-02-22 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0037_auto_20210217_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='level',
            field=models.CharField(blank=True, choices=[('', '---------'), ('ND1', 'ND1'), ('ND2', 'ND2'), ('ND3', 'ND3'), ('HND1', 'HND1'), ('HND2', 'HND2'), ('HND3', 'HND3'), ('100L', '100L'), ('200L', '200L'), ('300L', '300L'), ('400L', '400L')], max_length=10, null=True),
        ),
    ]