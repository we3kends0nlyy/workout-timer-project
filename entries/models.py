from django.db import models
from django.utils import timezone
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator





class Entry(models.Model):
    exercise = models.CharField(max_length=40)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

    class Meta:
        verbose_name_plural = "Entries"


class ExistingEntry1(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

class ExistingEntry2(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

class ExistingEntry3(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

class ExistingEntry4(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

class ExistingEntry5(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise