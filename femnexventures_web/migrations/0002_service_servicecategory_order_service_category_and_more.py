# Generated by Django 5.1.7 on 2025-03-18 07:38

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('femnexventures_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='service name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('service_type', models.CharField(choices=[('account_sale', 'Account Sale'), ('boost', 'Boost Service'), ('account_creation', 'Account Creation')], max_length=20, verbose_name='service type')),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per unit')),
                ('available_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='available stock')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='category name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/', verbose_name='category image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'service category',
                'verbose_name_plural': 'service categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='total price')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='status')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='femnexventures_web.service', verbose_name='service')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='femnexventures_web.servicecategory', verbose_name='category'),
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_images/', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='femnexventures_web.service', verbose_name='service')),
            ],
            options={
                'verbose_name': 'service image',
                'verbose_name_plural': 'service images',
                'ordering': ['created_at'],
            },
        ),
    ]
