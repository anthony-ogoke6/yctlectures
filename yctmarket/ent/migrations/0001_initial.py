# Generated by Django 2.1 on 2020-04-16 17:18

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('duration', models.CharField(max_length=10)),
                ('bodysnippet', models.TextField(blank=True, default='', null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('vid', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(editable=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('status', models.CharField(choices=[('', '---------'), ('draft', 'Draft'), ('published', 'Published')], max_length=10)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('category', models.CharField(choices=[('', '---------'), ('Agriculture & Food', 'Agriculture & Food'), ('Animals & Pets', 'Animals & Pets'), ('Babies & Kids', 'Babies & Kids'), ('Commercial Equipment & Tool', 'Commercial Equipment & Tool'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Health & Beauty', 'Health & Beauty'), ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'), ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'), ('Property', 'Property'), ('Repair & Construction', 'Repair & Construction'), ('Seeking Work - CVs', 'Seeking Work - CVs'), ('Services', 'Services'), ('Sport, Art & Outdoors', 'Sport, Art & Outdoors'), ('Vehicles', 'Vehicles')], max_length=100)),
                ('description', models.TextField()),
                ('video', models.FileField(blank=True, null=True, upload_to='')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('bodysnippet', models.TextField(blank=True, default='', null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('image2', models.ImageField(blank=True, null=True, upload_to='')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('duration', models.PositiveIntegerField(blank=True, choices=[('', '---------'), (7, '1 Week'), (14, '2 Weeks'), (28, '3 Weeks'), (31, '1 Month'), (366, '1 Year')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ent.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('status', models.CharField(choices=[('', '---------'), ('draft', 'Draft'), ('published', 'Published')], max_length=10)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('category', models.CharField(choices=[('', '---------'), ('Agriculture & Food', 'Agriculture & Food'), ('Animals & Pets', 'Animals & Pets'), ('Babies & Kids', 'Babies & Kids'), ('Commercial Equipment & Tool', 'Commercial Equipment & Tool'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Health & Beauty', 'Health & Beauty'), ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'), ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'), ('Property', 'Property'), ('Repair & Construction', 'Repair & Construction'), ('Seeking Work - CVs', 'Seeking Work - CVs'), ('Services', 'Services'), ('Sport, Art & Outdoors', 'Sport, Art & Outdoors'), ('Vehicles', 'Vehicles')], max_length=100)),
                ('description', models.TextField()),
                ('video', models.FileField(blank=True, null=True, upload_to='')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('bodysnippet', models.TextField(blank=True, default='', null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('image2', models.ImageField(blank=True, null=True, upload_to='')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('duration', models.PositiveIntegerField(blank=True, choices=[('', '---------'), (7, '1 Week'), (14, '2 Weeks'), (28, '3 Weeks'), (31, '1 Month'), (366, '1 Year')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseReference',
            fields=[
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_reference_number', models.CharField(max_length=200)),
            ],
        ),
    ]
