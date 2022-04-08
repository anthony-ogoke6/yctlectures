# Generated by Django 2.1 on 2021-03-11 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_remove_departmentalaccess_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentalAccessLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=800, null=True)),
            ],
            options={
                'verbose_name': 'Departmental Level Access',
                'verbose_name_plural': 'Departmental Level Access',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='level',
            field=models.CharField(blank=True, choices=[('N1', 'ND1'), ('N2', 'ND2'), ('N3', 'ND3'), ('H1', 'HND1'), ('H2', 'HND2'), ('H3', 'HND3'), ('100', '100L'), ('200', '200L'), ('300', '300L'), ('400', '400L')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='departmentalaccesslevel',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Department_level', to='learn.Department'),
        ),
    ]
