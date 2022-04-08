# Generated by Django 2.1 on 2021-08-06 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0040_auto_20210731_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentalAccessLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=800, null=True)),
                ('advert_images', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_level', to='ent.AdvertImages')),
            ],
            options={
                'verbose_name': 'Email Level Notification',
                'verbose_name_plural': 'Email Level Notification',
            },
        ),
    ]
