# Generated by Django 2.1 on 2021-07-31 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0039_remove_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='amountInDols',
        ),
        migrations.RemoveField(
            model_name='post',
            name='amountInDols',
        ),
    ]
