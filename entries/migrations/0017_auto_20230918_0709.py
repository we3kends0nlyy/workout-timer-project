# Generated by Django 3.2.1 on 2023-09-18 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0016_auto_20230918_0707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'Entries'},
        ),
        migrations.RemoveField(
            model_name='entry',
            name='workout',
        ),
        migrations.DeleteModel(
            name='Workout',
        ),
    ]