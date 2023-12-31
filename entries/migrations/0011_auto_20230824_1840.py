# Generated by Django 3.2.1 on 2023-08-24 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0010_auto_20230824_1655'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Time',
        ),
        migrations.DeleteModel(
            name='Workouts',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='title',
            new_name='workout',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='date_created',
        ),
        migrations.AddField(
            model_name='entry',
            name='minutes',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='seconds',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
