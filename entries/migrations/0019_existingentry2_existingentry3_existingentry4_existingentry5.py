# Generated by Django 3.2.1 on 2023-09-19 15:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0018_existingentry1'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExistingEntry2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=200)),
                ('order_in_workout', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('seconds', models.CharField(max_length=30)),
                ('minutes', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ExistingEntry3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=200)),
                ('order_in_workout', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('seconds', models.CharField(max_length=30)),
                ('minutes', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ExistingEntry4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=200)),
                ('order_in_workout', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('seconds', models.CharField(max_length=30)),
                ('minutes', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ExistingEntry5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=200)),
                ('order_in_workout', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('seconds', models.CharField(max_length=30)),
                ('minutes', models.CharField(max_length=30)),
            ],
        ),
    ]
