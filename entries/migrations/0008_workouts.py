# Generated by Django 3.2.1 on 2023-08-22 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0007_time_minutes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout', models.CharField(max_length=200)),
                ('seconds', models.CharField(max_length=30)),
                ('minutes', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Workouts',
            },
        ),
    ]
