# Generated by Django 2.1 on 2021-03-06 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_auto_20210304_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentalAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=800, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Department_courses', to='learn.Department')),
            ],
            options={
                'verbose_name': 'Departmental Access',
                'verbose_name_plural': 'Departmental Access',
            },
        ),
    ]