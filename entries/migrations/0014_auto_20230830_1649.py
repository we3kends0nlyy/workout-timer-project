# Generated by Django 3.2.1 on 2023-08-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0013_auto_20230830_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='minutes',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='entry',
            name='seconds',
            field=models.CharField(max_length=30),
        ),
    ]
