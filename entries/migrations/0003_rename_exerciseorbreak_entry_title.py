# Generated by Django 3.2.1 on 2023-08-19 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_auto_20230819_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='ExerciseOrBreak',
            new_name='title',
        ),
    ]
