# Generated by Django 3.2.1 on 2023-09-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0019_existingentry2_existingentry3_existingentry4_existingentry5'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='exercise',
            field=models.CharField(max_length=30),
        ),
    ]
