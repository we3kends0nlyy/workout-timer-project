# Generated by Django 3.2.1 on 2023-08-24 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0008_workouts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='content',
        ),
    ]