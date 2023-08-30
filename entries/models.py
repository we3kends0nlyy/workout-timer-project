from django.db import models
from django.utils import timezone
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator





class Entry(models.Model):
    exercise = models.CharField(max_length=200)
    order_in_workout = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.exercise

    class Meta:
        verbose_name_plural = "Entries"
