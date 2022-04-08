# Generated by Django 2.1 on 2021-01-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_auto_20210103_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stores',
            name='category',
            field=models.CharField(choices=[('', '---------'), ('Agriculture & Food', 'Agriculture & Food'), ('Animals & Pets', 'Animals & Pets'), ('Babies & Kids', 'Babies & Kids'), ('Commercial Equipment & Tool', 'Commercial Equipment & Tool'), ('Electronics', 'Electronics'), ('Entertainment', 'Entertainment'), ('Fashion', 'Fashion'), ('Health & Beauty', 'Health & Beauty'), ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'), ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'), ('Property', 'Property'), ('Repair & Construction', 'Repair & Construction'), ('Seeking Work - CVs', 'Seeking Work - CVs'), ('Services', 'Services'), ('Sport, Art & Outdoors', 'Sport, Art & Outdoors'), ('Vehicles', 'Vehicles')], max_length=100),
        ),
    ]