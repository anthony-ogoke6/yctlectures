# Generated by Django 2.1 on 2021-07-31 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_auto_20210731_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('', '---------'), ('draft', 'Draft'), ('published', 'Published')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_in_store', to='shops.Stores'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='category',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Agriculture & Food', 'Agriculture & Food'), ('Animals & Pets', 'Animals & Pets'), ('Babies & Kids', 'Babies & Kids'), ('Commercial Equipment & Tool', 'Commercial Equipment & Tool'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Health & Beauty', 'Health & Beauty'), ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'), ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'), ('Property', 'Property'), ('Repair & Construction', 'Repair & Construction'), ('Seeking Work - CVs', 'Seeking Work - CVs'), ('Services', 'Services'), ('Sport, Art & Outdoors', 'Sport, Art & Outdoors'), ('Vehicles', 'Vehicles')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_owner_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shops',
            name='status',
            field=models.CharField(blank=True, choices=[('', '---------'), ('draft', 'Draft'), ('published', 'Published')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='storename',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='view_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='category',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Agriculture & Food', 'Agriculture & Food'), ('Animals & Pets', 'Animals & Pets'), ('Babies & Kids', 'Babies & Kids'), ('Commercial Equipment & Tool', 'Commercial Equipment & Tool'), ('Electronics', 'Electronics'), ('Entertainment', 'Entertainment'), ('Fashion', 'Fashion'), ('Health & Beauty', 'Health & Beauty'), ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'), ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'), ('Property', 'Property'), ('Repair & Construction', 'Repair & Construction'), ('Seeking Work - CVs', 'Seeking Work - CVs'), ('Services', 'Services'), ('Sport, Art & Outdoors', 'Sport, Art & Outdoors'), ('Vehicles', 'Vehicles')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_owner_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stores',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='status',
            field=models.CharField(blank=True, choices=[('', '---------'), ('draft', 'Draft'), ('published', 'Published')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='storename',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stores',
            name='view_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
