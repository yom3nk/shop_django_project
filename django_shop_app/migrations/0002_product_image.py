# Generated by Django 5.0.1 on 2024-03-31 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_shop_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='blank.jpg', upload_to='product_images/'),
        ),
    ]
